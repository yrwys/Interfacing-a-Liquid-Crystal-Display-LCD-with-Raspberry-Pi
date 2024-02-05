import I2C_LCD_driver
from time import sleep
import RPi.GPIO as GPIO

# Constants for LCD display positions
LCD_LINE1 = 1
LCD_LINE2 = 2
LCD_LINE3 = 3
LCD_LINE4 = 4

# Constants for button pins
BUTTON1_PIN = 20
BUTTON2_PIN = 21

def initialize_components():
    """Initialize LCD and GPIO components."""
    mylcd = I2C_LCD_driver.lcd()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    return mylcd

def read_questions(file_path):
    """Read questions from a file and return as a list."""
    try:
        with open(file_path, 'r') as file:
            questions = file.readlines()
        return questions
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return []

def display_question(mylcd, question, option1, option2, score):
    """Display the question, options, and score on the LCD."""
    mylcd.lcd_clear()
    mylcd.lcd_display_string(question, LCD_LINE3, 6)
    mylcd.lcd_display_string(option1, LCD_LINE4, 2)
    mylcd.lcd_display_string(option2, LCD_LINE4, 16)
    mylcd.lcd_display_string(f"Score: {max(score, 0)}", LCD_LINE1, 6)

def main():
    """Main function to run the trivia quiz game."""
    mylcd = initialize_components()
    questions = read_questions("quizfile.txt")
    total_questions = len(questions)

    if not questions:
        return

    while True:
        mylcd.lcd_clear()
        mylcd.lcd_display_string("   Quick Math   ", LCD_LINE1, 2)
        mylcd.lcd_display_string("Press any button", LCD_LINE3, 2)
        mylcd.lcd_display_string("    to start    ", LCD_LINE4, 2)

        while GPIO.input(BUTTON1_PIN) and GPIO.input(BUTTON2_PIN):
            pass

        score = 0
        question_number = 0

        for question in questions:
            question_number += 1
            question, option1, option2, answer = question.strip().split(";")
            display_question(mylcd, question, option1, option2, score)

            while GPIO.input(BUTTON1_PIN) and GPIO.input(BUTTON2_PIN):
                pass

            if GPIO.input(BUTTON1_PIN) == GPIO.LOW and answer == "op1":
                score = max(0, score + 1)
            elif GPIO.input(BUTTON2_PIN) == GPIO.LOW and answer == "op2":
                score = max(0, score + 1)

        mylcd.lcd_clear()
        mylcd.lcd_display_string("GAME OVER!", LCD_LINE1, 5)
        mylcd.lcd_display_string(f"Score: {max(score, 0)} of {total_questions}", LCD_LINE3, 3)
        sleep(5)

if __name__ == "__main__":
    main()
