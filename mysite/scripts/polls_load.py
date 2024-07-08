import csv  # https://docs.python.org/3/library/csv.html}

from polls.models import Question, Choice
from django.utils import timezone


def run():
    print("=== Polls Loader")

    Choice.objects.all().delete()
    Question.objects.all().delete()
    print("=== Objects deleted")

    fhand = open('scripts/dj4e_batch.csv')
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    for row in reader:
        print('XXXXXXXXX:', row, '   XXXXXXX')
        question = Question(question_text=row[0], pub_date=timezone.now())
        question.save()

        print(question.id, question)

        count_choices = len(row[1:])
        while count_choices > 0:
            #print(count_choices)
            choice_text = row[count_choices]
            choice = Choice(question=question, choice_text=choice_text)
            print(question.id, choice)
            choice.save()
            count_choices = count_choices - 1





        # Loop through the choice strings in row[1:] and add each choice,
        # connect it to the question and save it
    print("=== Load Complete")
