
# Load necessary libraries
library(rpart)
library(rpart.plot)

# Training a decision tree in R

# Load the iris dataset
iris_df <- datasets::iris

# Set the train-test split ratio
train_ratio <- 0.8
n <- nrow(iris_df)
n_train <- round(train_ratio * n)

# Generate random indices for train-test split
set.seed(123)  
train_indices <- sample(1:n, n_train)
iris_train <- iris_df[train_indices, ]
iris_test <- iris_df[-train_indices, ]

# Train the decision tree model to predict "Species"
dt_model <- rpart(
  formula = Species ~ .,
  data = iris_train,
  method = "class",
  control = rpart.control(minsplit = 3) # Control parameters for decision tree
)

