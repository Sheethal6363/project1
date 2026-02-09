import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

DATASET_PATH = r'c:\project1\Three Classes'

train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical'
)

print("Class Indices:", train_generator.class_indices)
