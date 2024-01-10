
# Packages to install in R
packages_to_install <- c("rpart.plot", "reticulate", "inTrees", "caTools", "randomForest", "kernlab")
install.packages(packages_to_install)

library("reticulate")

# Define the Python version
version <- "3.9.12"

# Install Python version and create a new environment
install_python(version)
virtualenv_create("r-reticulate", version = version)
use_virtualenv("r-reticulate")

# Install required Python packages
py_install(c("z3-solver","numpy","pandas"))
