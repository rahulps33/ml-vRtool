
# Load necessary libraries
library(inTrees)
library(caTools)
library(randomForest)
library(reticulate)

# Activate the specific Python environment
use_virtualenv("r-reticulate")

# Function to extract rules from a random forest model and solve using a z3 solver
rf_solver_r <- function(model, referal_input, epsilon) {
  
  # Extract list of trees from random forest
  treeList <- RF2List(model)
  
  # Function to extract a single tree
  extractSingleTree <- function(treeList, treeNumber) {
    singleTreeList <- list(ntree = 1, list = list(treeList$list[[treeNumber]]))
    return(singleTreeList)
  }
  
  # Extract rules for each tree in the forest
  num_trees <- model$ntree
  rf_rules <- matrix(nrow=0, ncol = 6)
  
  for (treeNumber in 1:num_trees) {
    singleTreeList <- extractSingleTree(treeList, treeNumber)
    ruleExec0 <- extractRules(singleTreeList,X,random = FALSE)  # transform to R-executable conditions
    ruleMetric <- getRuleMetric(ruleExec0,X,target)
    ruleMetric <- cbind(ruleMetric,treeNumber)
    colnames(ruleMetric)[ncol(ruleMetric)] <- "ntree"
    rf_rules <- rbind(rf_rules, ruleMetric)
  }
  
  # Remove unnecessary columns and adjust column names
  rf_rules <- rf_rules[, !colnames(rf_rules) %in% c("len", "freq", "err")]
  
  col_names <- names(X)
  for (i in 1:length(col_names)) {
    rf_rules[, "condition"] <- sapply(rf_rules[, "condition"], function(x) gsub(paste0("X\\[,",i,"\\]"), col_names[i], x))
  }
  
  # Write rules and sample input to CSV files
  write.csv(rf_rules, "temp_data//rf_rules.csv", row.names=FALSE)
  write.csv(referal_input, "temp_data//sample_input.csv", row.names=FALSE)
  
  # Run the random forest solver in z3
  solver <- py_run_file("ml_solvers//z3_solvers//rf_solver.py")
  solver$rf_solver(epsilon)
  
  # Remove temporary CSV files
  unlink("temp_data//rf_rules.csv")
  unlink("temp_data//sample_input.csv")
}





