
# Load necessary libraries
library(kernlab)

# Training a binary linear SVM model in R

# Binary data generation
set.seed(42)
X_class_a <- matrix(rnorm(0, sd = 0.5, n = 80), 40, 2)
X_class_b <- matrix(rnorm(1, sd = 0.5, n = 80), 40, 2)
X <- rbind(X_class_a, X_class_b)
y <- rep(c(-1, 1), c(40, 40))
# Creating a dataframe with features (X1, X2) and the target variable (y)
df_linear <- data.frame(X1 = X[,1], X2 = X[,2], y = factor(y))

# Training a binary linear SVM model using the 'ksvm' function
svm_bin_model <- ksvm(y ~ X1 + X2,
                data = df_linear,
                type = "C-svc", # "C-svc" specifies a C-support vector classification type
                kernel = "vanilladot") # kernel = "vanilladot" specifies the linear kernel