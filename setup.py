from setuptools import setup, find_packages

setup(
    name="pneumonia_detector",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pyautogui==0.9.52",
        "pillow==8.2.0",
        "tkcap==0.0.4",
        "pydicom==2.2.2",
        "img2pdf==0.4.1",
        "opencv-python==4.5.3.56",
        "matplotlib==3.4.3",
        "pandas==1.3.3",
        "tensorflow==2.4.0",
        "python-xlib==0.30"
    ]
)