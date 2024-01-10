
# Load necessary libraries
library(keras)
library(reticulate)

#loading the keras inbuilt mnist dataset
data <- dataset_mnist()

#Training Data
train_x <- data$train$x
train_y <- data$train$y

#Test Data
test_x <- data$test$x
test_y <- data$test$y

# Reshape & rescale
train_x <- train_x / 255
test_x <- test_x / 255

# One hot encoding
train_y <- to_categorical(train_y, 10)
test_y <- to_categorical(test_y, 10)

# Model architecture
model <- keras_model_sequential(input_shape = c(28, 28)) %>%
  layer_flatten() %>%
  layer_dense(128, activation = "relu") %>%
  layer_dropout(0.2) %>%
  layer_dense(10)

summary(model) # Display model summary

# Compile the model
model %>%
  compile(loss = loss_categorical_crossentropy(from_logits = TRUE),
          optimizer = optimizer_rmsprop(),
          metrics = 'accuracy')

# Fit the model
history <- model %>%
  fit(train_x,
      train_y,
      epochs = 2,
      batch_size = 32,
      validation_split = 0.2)

print(summary(history)) # Display summary of model training

