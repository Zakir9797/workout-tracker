# Workout Tracker

A simple desktop application to log and visualize your workout progress.

## Features

- Add exercises with sets, reps, and calories burned
- View workout history and summaries
- Clear form with one click
- Visualize your progress with graphs
- Lightweight and easy to use
- Built with Python and Tkinter

## Installation

1. **Clone or download the repository**  
git clone https://github.com/yourusername/workout-tracker.git

2. **Install dependencies**  
Make sure you have Python 3.10+ installed  
pip install -r requirements.txt

3. **Run the application**  
python main.py

## Build .EXE (Optional)

To generate a standalone executable using PyInstaller:

pyinstaller --noconsole --onefile --icon=icon.ico main.py

The `.exe` will be located in the `dist/` folder.

## Screenshots

| Input Form | Summary View | Graph |
|------------|---------------|-------|
| ![screenshot1](screenshots/form.png) | ![screenshot2](screenshots/summary.png) | ![screenshot3](screenshots/graph.png) |

## Folder Structure

workout-tracker/
│
├── main.py
├── requirements.txt
├── icon.ico
├── data/
├── dist/
└── build/

## Technologies

- Python 3
- Tkinter
- Matplotlib
- CSV for data storage

## Contact

For questions or feedback, feel free to contact me via GitHub or email.


