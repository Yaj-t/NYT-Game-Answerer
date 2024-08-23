from playwright.sync_api import sync_playwright, expect
import requests

def fetch_data():
    url = "https://www.nytimes.com/svc/crosswords/v6/puzzle/mini.json"
    payload = {}
    headers = {}
    return requests.request("GET", url, headers=headers, data=payload).json()

def answer_mini():
  response = fetch_data()
  cells = response['body'][0]['cells']
  dimensions = response['body'][0]['dimensions']
  width = dimensions['width']

  letters =  [cell.get('answer') for cell in cells]
  matrix = [letters[i:i+width] for i in range(0, len(letters), width)]
  answers = [''.join([letter for letter in row if letter is not None]) for row in matrix]
    
  return answers


def main():
    answers = answer_mini()
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context(record_video_dir='videos/', viewport={'width': 1280, 'height': 720})

    page = context.new_page()
    page.goto('https://www.nytimes.com/crosswords/game/mini')
    page.get_by_role("button").and_(page.get_by_text('Play without an account')).click()
    page.wait_for_load_state()

    for i, answer in enumerate(answers):
        page.keyboard.type(answer)
        if i < len(answers) - 1:
            page.keyboard.press('Enter')
    page.wait_for_load_state()
    page.screenshot(path='score.png')
    page.close()
    context.close()
    browser.close()

if __name__ == "__main__":
    main()

