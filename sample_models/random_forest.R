
# Load necessary libraries
library(randomForest)

# Training a random forest in R

# Load Iris dataset
data(iris)

# Separate predictor variables (X) and target variable (Species)
X <- iris[, 1:(ncol(iris) - 1)]
target <- iris[, "Species"]

# Train the random forest model to predict "Species"
rf_model <- randomForest(X, 
                   as.factor(target), 
                   ntree = 5) # Set ntree = 5 to grow 5 trees in the random forest