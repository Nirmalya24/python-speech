import random
import time
import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # setup the response  object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response['transcription'] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response['success'] = False
        response['error'] = "API Unavailable"
    except sr.UnknownValueError:
        response['error'] = "Unable to recognize speech"

    return response

if __name__ == "__main__":
    WORDS = ["apple", "banana", "grape", "orange", "mango", "lemon"]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # get a random word from the list
    word = random.choice(WORDS)

    # format instruction string
    instructions = (
        "I am thinking of one of these words: \n"
        "{words}\n"
        "You have {n} tries to guess which one. \n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)

    # show instructions and wait for 3 seconds before starting the game
    print(instructions)
    time.sleep(3)

    guess =""

    for i in range(NUM_GUESSES):
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Speak!'.format(j+1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess['transcription']:
                break
            if not guess['success']:
                break
            print("I didn't catch that. What did you say?\n")

        # stop game if error
        if guess['error']:
            print("ERROR: {}".format(guess['error']))
            break

        # show transcription to user
        print("You said: {}".format(guess['transcription']))

        # determine guess and if any attempts remain
        guess_is_correct = guess['trascription'].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        if guess_is_correct:
            print("Correct, you win!".format(word))
            break
        elif user_has_more_attempts:
            print("Incorrect, try again\n")
        else:
            print('Sorry, you lose!\nI was thinking of {}'.format(word))
            break