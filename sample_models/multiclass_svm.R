
# Load necessary libraries
library(kernlab)

# Training a linear multiclass SVM in R

# Load the iris dataset
data(iris)

# Train a linear multiclass SVM model to predict "Species"
svm_model <- ksvm(
  Species ~ .,
  data = iris,
  type = "C-svc", # "C-svc" specifies a C-support vector classification type
  kernel = "vanilladot", # "vanilladot" is the kernel function (linear kernel in this case)
  scale = FALSE) # Set scale = FALSE to avoid scaling the data
