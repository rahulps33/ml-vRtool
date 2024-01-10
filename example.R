

# ML solvers
# ----------------------------------------------------------------------------
# Install requirements for ML solvers
source("requirements//requirements_ml.R")


# Decision tree solver
# ----------------------------------------------------------------------------
# Train decision tree model
source("sample_models//decision_tree.R")

# Call decision tree solver
source("ml_solvers//dt_solver.R")
dt_solver_r(dt_model, iris_df[1,], 1.4)


# Random forest solver
# ----------------------------------------------------------------------------
# Train random forest model
source("sample_models//random_forest.R")

# Call random forest solver
source("ml_solvers//rf_solver.R")
rf_solver_r(rf_model, iris[1,], 1.1)


# SVM solver  
# ----------------------------------------------------------------------------

# Call SVM solver
source("ml_solvers//svm_solver.R")

# Train SVM binary model
source("sample_models//binary_svm.R")
# Call SVM - Binary solver
svmbin_solver_r(svm_bin_model, df_linear[1,], 1.1)

# Train SVM multiclass model
source("sample_models//multiclass_svm.R")
# Call SVM - Multiclass solver
svm_solver_r(svm_model, iris[1,], 1.1)


# NN solver - Marabou
# ----------------------------------------------------------------------------

# NN sample model
source("sample_models//nn_sample.R")

# Call Marabou from NN solver
source("nn_solvers//nn_solver.R")

image = train_x[1,,]
class = train_y[1]
marabou_solver_r(model, 0.1, image, class)
