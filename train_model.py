import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import os
import json
import traceback
import sys

# Redirect stderr to a file for capturing
sys.stderr = open(r'c:\project1\error_log.txt', 'w')

try:
    # Define paths
    DATASET_PATH = r'c:\project1\Three Classes'
    MODEL_SAVE_PATH = r'c:\project1\model.h5'
    INDICES_SAVE_PATH = r'c:\project1\class_indices.json'

    # Parameters
    IMG_HEIGHT = 128
    IMG_WIDTH = 128
    BATCH_SIZE = 32
    EPOCHS = 30 

    # Data Augmentation 
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )

    print(f"Loading data from {DATASET_PATH}...")

    train_generator = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    validation_generator = train_datagen.flow_from_directory(
        DATASET_PATH,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    # Save class indices
    class_indices = train_generator.class_indices
    start_index_mapping = {v: k for k, v in class_indices.items()}
    with open(INDICES_SAVE_PATH, 'w') as f:
        json.dump(start_index_mapping, f)
    
    # Enhanced Model Architecture
    model = Sequential([
        # Explicit input layer
        Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        
        Conv2D(32, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        
        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(2, 2),

        Conv2D(256, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(2, activation='softmax') # CHANGED TO 2 CLASSES
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()

    # Callbacks
    checkpoint = ModelCheckpoint(MODEL_SAVE_PATH, monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # Training
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        callbacks=[checkpoint, early_stop]
    )

    print("Training finished.")

except Exception:
    traceback.print_exc()
