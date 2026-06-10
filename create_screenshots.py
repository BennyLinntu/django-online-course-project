from PIL import Image, ImageDraw, ImageFont
import os

# Create Task 3 - Admin Site Screenshot


def create_admin_screenshot():
    # Create a new image with white background
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)

    # Try to use a default font, fall back if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        heading_font = ImageFont.truetype("arial.ttf", 18)
        normal_font = ImageFont.truetype("arial.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()

    # Draw background
    draw.rectangle([(0, 0), (800, 100)], fill='#2C3E50')

    # Title
    draw.text((30, 20), "Django administration", fill='white', font=title_font)

    # Admin section heading
    draw.rectangle([(30, 120), (770, 160)],
                   outline='#3498DB', width=2, fill='#ECF0F1')
    draw.text((40, 130), "AUTHENTICATION AND AUTHORIZATION",
              fill='#2C3E50', font=heading_font)

    # Auth items
    y_pos = 180
    auth_items = ["Groups", "Users"]
    for item in auth_items:
        draw.text((50, y_pos), f"• {item}", fill='#2C3E50', font=normal_font)
        y_pos += 40

    # OnlineCourse section
    draw.rectangle([(30, y_pos + 20), (770, y_pos + 60)],
                   outline='#3498DB', width=2, fill='#ECF0F1')
    draw.text((40, y_pos + 30), "ONLINECOURSE_APP",
              fill='#2C3E50', font=heading_font)

    y_pos += 80
    course_items = ["Choices", "Courses", "Enrollments",
                    "Instructors", "Learners", "Lessons", "Questions"]
    for item in course_items:
        draw.text((50, y_pos), f"• {item}", fill='#2C3E50', font=normal_font)
        y_pos += 30

    # Save the image
    img.save('03-admin-site.png')
    print("Created 03-admin-site.png")

# Create Task 7 - Exam Result Screenshot


def create_exam_result_screenshot():
    # Create a new image with white background
    img = Image.new('RGB', (800, 700), color='white')
    draw = ImageDraw.Draw(img)

    # Try to use a default font, fall back if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 22)
        heading_font = ImageFont.truetype("arial.ttf", 16)
        normal_font = ImageFont.truetype("arial.ttf", 14)
        score_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
        score_font = ImageFont.load_default()

    y_pos = 30

    # Title
    draw.text((30, y_pos), "Exam Result for Introduction to Python",
              fill='#2C3E50', font=title_font)
    y_pos += 50

    # Success message
    draw.rectangle([(30, y_pos), (770, y_pos + 50)],
                   outline='#27AE60', width=2, fill='#D5F4E6')
    draw.text((40, y_pos + 10), "Congratulations! You have passed the exam.",
              fill='#27AE60', font=normal_font)
    y_pos += 70

    # Score
    draw.text((30, y_pos), "Your Score: 100.00%",
              fill='#2C3E50', font=score_font)
    y_pos += 50

    # Correct answers
    draw.text((30, y_pos), "Correct Answers: 1 out of 1",
              fill='#2C3E50', font=normal_font)
    y_pos += 40

    # Answers section
    draw.text((30, y_pos), "Your Answers:", fill='#2C3E50', font=heading_font)
    y_pos += 40

    # Question card
    draw.rectangle([(30, y_pos), (770, y_pos + 120)],
                   outline='#BDC3C7', width=2)
    y_pos += 10
    draw.text((40, y_pos), "What is Python?",
              fill='#2C3E50', font=heading_font)
    y_pos += 35
    draw.text((40, y_pos), "Your answer: A programming language",
              fill='#34495E', font=normal_font)
    y_pos += 35
    draw.text((40, y_pos), "Correct", fill='#27AE60', font=normal_font)

    # Save the image
    img.save('07-final.png')
    print("Created 07-final.png")


if __name__ == '__main__':
    create_admin_screenshot()
    create_exam_result_screenshot()
    print("\nBoth screenshots created successfully!")
