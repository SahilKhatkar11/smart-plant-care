# 🌱 Smart Plant Care Assistant

An AI-powered plant health monitoring tool that helps users detect plant diseases and suggests care actions using simple image classification techniques — built entirely **locally** using Python, TensorFlow, and Streamlit.

> 🔧 Built for: Microsoft AI + Azure (Edunet Foundation) Internship
> 🚫 No cloud dependencies (runs 100% locally)

---

## 📌 Table of Contents

* [About the Project](#about-the-project)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Folder Structure](#folder-structure)
* [How It Works](#how-it-works)
* [Setup Instructions](#setup-instructions)
* [How to Use](#how-to-use)
* [Screenshots](#screenshots)
* [Future Scope](#future-scope)
* [Credits](#credits)

---

## 🌿 About the Project

The **Smart Plant Care Assistant** aims to support home gardeners, farmers, and plant lovers by providing instant health diagnosis of plants via leaf image classification. It can identify whether a plant is **healthy** or **unhealthy**, and recommend basic care tips such as watering, increasing sunlight, or checking for disease.

---

## ✨ Features

* 🔍 Detect plant health using leaf images (Healthy / Unhealthy)
* 📷 Simple web interface to upload plant photos
* 💡 Gives plant care suggestions based on prediction
* 🧠 Built with a custom-trained Convolutional Neural Network (CNN)
* 🖥️ Works offline without requiring Azure or internet
* 📊 Future scope: support for more diseases, sensors, and voice interface

---

## 🧰 Tech Stack

| Component      | Tool/Library                                                                  |
| -------------- | ----------------------------------------------------------------------------- |
| Programming    | Python 3.10+                                                                  |
| ML Framework   | TensorFlow + Keras                                                            |
| Image Handling | OpenCV                                                                        |
| UI Interface   | Streamlit                                                                     |
| Dataset Source | [PlantVillage - Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease) |
| Others         | NumPy, Pandas, Matplotlib                                                     |

---

## 📁 Folder Structure

```
smart-plant-care/
├── data/
│   ├── healthy/              # Images of healthy leaves
│   └── unhealthy/            # Images of unhealthy/diseased leaves
├── model/
│   └── plant_health_model.h5 # Saved trained model
├── notebooks/
│   └── train_model.ipynb     # Jupyter notebook to train model
├── app/
│   └── app.py                # Streamlit app UI
├── utils/
│   └── preprocess.py         # Image loading & preprocessing (optional)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## ⚙️ How It Works

1. **Image Collection**
   You gather images of plant leaves labeled as `healthy` or `unhealthy`.

2. **Model Training**
   A CNN model is trained using TensorFlow on this dataset.

3. **Prediction**
   The Streamlit app allows users to upload a leaf image. The model predicts the health status and gives suggestions.

4. **Suggestion Engine**
   Based on the output class (healthy/unhealthy), a care suggestion is shown to the user.

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-plant-care.git
cd smart-plant-care
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare Dataset

Download and organize images into:

```
data/
├── healthy/
├── unhealthy/
```

You can get sample data from: [PlantVillage Dataset](https://www.kaggle.com/datasets/emmarex/plantdisease)

### 5. Train the Model

Open the notebook:

```bash
jupyter notebook notebooks/train_model.ipynb
```

Train and export the model to `model/plant_health_model.h5`.

### 6. Run the App

```bash
streamlit run app/app.py
```

---

## 🧑‍🌾 How to Use

1. Run the app.
2. Upload an image of a plant leaf.
3. View the predicted result (Healthy / Unhealthy).
4. Read suggested care actions.
5. Optionally, enter light or moisture details for more accurate tips.

---

## 🖼️ Screenshots (You can add later)

```
[Image 1: App Upload Page]
[Image 2: Prediction Result]
[Image 3: Suggestions Shown]
```

---

## 🚀 Future Scope

* 🪴 Detect specific plant diseases (multi-class model)
* 🌦️ Integrate weather API for environment-based care tips
* 🌡️ Use real sensors for moisture, temperature, pH
* 📱 Convert to mobile app using Streamlit Sharing or Flutter
* 🎙️ Voice assistant using Azure OpenAI (if available)

---

## 🙏 Credits

* Dataset: [PlantVillage by Penn State University](https://www.kaggle.com/datasets/emmarex/plantdisease)
* Developed as part of **Microsoft AI + Azure Internship (Edunet Foundation)**
* Developer: *Sahil Khatkar* (GitHub: [@SahilKhatkar11](https://github.com/SahilKhatkar11))
