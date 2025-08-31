# Pomodoro Timer

A desktop application that implements the Pomodoro Technique for time management, helping you stay focused and productive.

## Features
- **Work Sessions**: 25-minute focused work periods
- **Short Breaks**: 5-minute breaks between work sessions
- **Long Breaks**: 15-minute breaks after 4 work sessions
- **Visual Timer**: Clear countdown display with status indicators
- **Sound Alerts**: Audio notifications when timers complete
- **Customizable**: Adjust work and break durations
- **Session Tracking**: Counts completed Pomodoro sessions

## How to Run
```bash
python main.py
```

## Usage
1. **Start**: Click "Start" to begin the timer
2. **Pause**: Click "Pause" to temporarily stop the timer
3. **Reset**: Click "Reset" to restart the current session
4. **Settings**: Adjust work, break, and long break durations

## Pomodoro Technique
The technique involves:
1. 25 minutes of focused work
2. 5-minute short break
3. After 4 work sessions, take a 15-minute long break
4. Repeat the cycle

## Sound Alerts
The timer uses system beeps to alert you when:
- Work session completes
- Break session completes

## Customization
You can customize:
- Work duration (1-60 minutes)
- Short break duration (1-30 minutes)
- Long break duration (1-30 minutes)

## Note
This application uses Tkinter for the GUI and winsound for audio alerts (Windows only). For other operating systems, you may need to modify the sound functionality.
