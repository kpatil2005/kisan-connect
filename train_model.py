"""
Plant Disease Detection Model Training Script
Uses TensorFlow/Keras with MobileNetV2 for efficient prediction
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import json
import os

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 1
TRAIN_DIR = '../train'
VALID_DIR = '../valid'
MODEL_PATH = 'app/ml_models/plant_disease_model.h5'
CLASSES_PATH = 'app/ml_models/classes.json'

# Create model directory
os.makedirs('app/ml_models', exist_ok=True)

print("🌿 Plant Disease Detection Model Training")
print("=" * 50)

# Data Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

valid_datagen = ImageDataGenerator(rescale=1./255)

# Load Data
print("\n📂 Loading training data...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

print("\n📂 Loading validation data...")
valid_generator = valid_datagen.flow_from_directory(
    VALID_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Save class names
class_names = list(train_generator.class_indices.keys())
with open(CLASSES_PATH, 'w') as f:
    json.dump(class_names, f, indent=2)
print(f"\n✅ Found {len(class_names)} disease classes")

# Build Model using MobileNetV2
print("\n🏗️ Building model...")
base_model = keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(len(class_names), activation='softmax')
])

# Compile Model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\n📊 Model Summary:")
model.summary()

# Callbacks
callbacks = [
    keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=2)
]

# Train Model
print(f"\n🚀 Training model for {EPOCHS} epochs...")
history = model.fit(
    train_generator,
    validation_data=valid_generator,
    epochs=EPOCHS,
    callbacks=callbacks
)

# Save Model
model.save(MODEL_PATH)
print(f"\n✅ Model saved to {MODEL_PATH}")

# Evaluate
print("\n📈 Final Results:")
print(f"Training Accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")

print("\n✅ Training Complete!")
