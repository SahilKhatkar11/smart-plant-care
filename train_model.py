import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split

# Set random seed for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

def load_images_from_folder(folder, label):
    images = []
    labels = []
    for filename in os.listdir(folder):
        if filename.startswith('.'):  # Skip hidden files
            continue
        img_path = os.path.join(folder, filename)
        try:
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (224, 224))
                images.append(img)
                labels.append(label)
        except Exception as e:
            print(f"Error loading {img_path}: {str(e)}")
    return images, labels

def create_model():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])
    return model

def main():
    print("Loading images...")
    # Load data from directories
    healthy_images, healthy_labels = load_images_from_folder('data/healthy', 1)
    unhealthy_images, unhealthy_labels = load_images_from_folder('data/unhealthy', 0)

    print(f"Loaded {len(healthy_images)} healthy images and {len(unhealthy_images)} unhealthy images")

    # Combine datasets
    X = np.array(healthy_images + unhealthy_images)
    y = np.array(healthy_labels + unhealthy_labels)

    # Normalize pixel values
    X = X.astype('float32') / 255.0

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Creating and compiling model...")
    # Create and compile model
    model = create_model()
    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])

    print("Training model...")
    # Train the model
    history = model.fit(X_train, y_train,
                    epochs=20,
                    batch_size=32,
                    validation_data=(X_test, y_test))

    # Evaluate model on test set
    test_loss, test_accuracy = model.evaluate(X_test, y_test)
    print(f"\nTest accuracy: {test_accuracy:.4f}")
    print(f"Test loss: {test_loss:.4f}")

    # Create model directory if it doesn't exist
    os.makedirs('model', exist_ok=True)

    # Save the model
    model_save_path = 'model/plant_health_model.h5'
    model.save(model_save_path)
    print(f"\nModel saved to {model_save_path}")

if __name__ == "__main__":
    main() 