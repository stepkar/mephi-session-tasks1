import random


def _read_file_(file:str)-> list[str]:
  with open(file, 'r') as file:
    return [line.rstrip() for line in file if line.rstrip()]

'''
1. Обратный порядок слов в блоках текста

*Про вывод в задании ничего не сказано, но в критериях оценки есть. Пусть будет через точку :)
*В самом задании, предложения идут через перечисления (1,2,3 которые не копируются — соответственно не обрабатывал)
'''
def task1_reversed_blocks(file_path: str, block_size: int = 2)->list:
  lines = _read_file_(file_path)
  blocks = [lines[i:i+block_size] for i in range(0, len(lines), block_size)]
  reversed_blocks = [[' '.join(reversed(sentense.split(' '))) for sentense in block]
    for block in blocks
  ]
  for block in reversed_blocks:
    print('. '.join(block))
  return reversed_blocks


'''2. Сжатие строки'''
def task2_string_flatter(string: str):
    if len(string) <= 1:
      print(string)
      return string

    def compress(text: str) -> str:
      if not any(text[i] == text[i-1] for i in range(1,len(text))):
        return text
      comp = []
      counter = 1
      for i in range(1, len(text)):
        if text[i] == text[i -1]:
          counter +=1
        else:
          comp.append(text[i-1] + (str(counter) if counter>1 else ''))
          counter = 1
      comp.append(text[-1] + (str(counter) if counter>1 else ''))
      result = ''.join(comp)
      return result if len(result) < len(text) else text
    result = ''
    for i, part in enumerate(string.split(' ')):
      if i>0:
        result += ' '
      result += compress(part)
    print(result)
    return result


'''Проверка скобок'''
#Задача решена в рамках курса яндекс.алгоритмы)
def task3_is_correct_bracket(brackets:str):
  if brackets == '':
    return True
  if len(brackets)%2 != 0:
    return False

  def opposite_bracket(c:str):
    if c=='(': return ')'
    elif c=='[': return ']'
    else: return '}'

  from collections import deque
  stack = deque()
  for ch in brackets:
    if not stack or ch != opposite_bracket(stack[-1]):
      stack.append(ch)
    elif ch == opposite_bracket(stack[-1]):
      stack.pop()
  print(not stack)
  return not stack


'''Генератор паролей'''
def task4_random_pass() -> str:
  import random
  import string
  pass_length = ''
  while True:
    # >=3 потому что по условию надо минимум: букву+цифру+символ
    if pass_length.isdigit() and int(pass_length) >= 3:
      break
    pass_length = input('Задайте длину пароля больше 3: ')
  letters = string.ascii_letters
  digits = string.digits
  symbols = string.punctuation
  def random_choice(randint: int = None):
    if not randint: randint = random.randint(1,3)
    if randint == 1:
      return random.choice(letters)
    elif randint == 2:
      return random.choice(digits)
    elif randint == 3:
      return random.choice(symbols)
    return None

  #гарантируем условие — буква/цифра/символ:
  rand_pass = [random_choice(i) for i in range(1, 4)]

  for i in range (0, int(pass_length) - 3):
    rand_pass.append(random_choice())

  rand_pass = ''.join(rand_pass)
  print(f'Ваш пароль: {rand_pass}')
  return rand_pass


'''Почти палиндром'''
def task5_is_palindrom(text:str) ->bool:
  if len(text) < 2:
    print('False')
    return False
  lower = text.lower().replace(' ', '')
  if lower == lower[::-1]:
    print('True')
    return True

  #workflow:
  #сюда abcba по идее не должны попасть. Они уйдут в True выше.
  #Хотя abcbad могут:
  #TODO учесть что удалять нужно удалять 1 специфическую букву а не первую попавшуюся
  #TODO учесть что могут быть ещё abccbac. Значит проверяем все "длиной 1 или если %2 != 0": удаляем с этим условием
  #TODO abcbac — придётся перебирать удаления всех. Значит Counter не нужен.
  for i, char in enumerate(lower):
      temp_arr = list(lower)
      del temp_arr[i]
      if temp_arr == temp_arr[::-1]:
        print('True')
        return True
  print('False')
  return False

'''Задача Шредингера'''
def task6_shredinger(file_path: str, percent:int):
  if percent == 100:
    return ''
  lines = _read_file_(file_path)
  words = [word for line in lines for word in line.split(' ')]
  result_letters = [letter for word in words for letter in word if word != '...']
  initial_result_length = len(result_letters)
  needed_length_result = initial_result_length*(100-percent) //100

  result = words.copy()
  #если мы удалим слишком большое слово и окажется что с ним, мы ближе к нужному % чем без него, то сделаем откат
  temp_result = []
  while True:
    result_letters = [letter for word in result for letter in word if word != '...']
    result_length = len(result_letters)
    #current_words — чтобы не выбирать из ...
    current_words = [word for word in result if word != '...']
    if result_length > needed_length_result:
      temp_result = result.copy() # для отката можно было сохранять слово и позицию.
      result[result.index(random.choice(current_words))] = '...'
    else:
      temp_result_letters = [letter for word in temp_result for letter in word if word != '...']
      temp_result_length = len(temp_result_letters)
      temp_diff = temp_result_length-needed_length_result
      result_diff = result_length-needed_length_result
      # print(f'temp diff:{temp_diff}')
      # print(f'result diff:{result_diff}')
      if abs(temp_diff) < abs(result_diff):
        #откат
        print(f'(удалено {100 - (temp_result_length * 100 // initial_result_length)}%)')
        print(' '.join(temp_result))
        break
      else:
        print(f'(удалено {100 - (result_length * 100 // initial_result_length)}%)')
        print(' '.join(result))
        break
  return None


if __name__ == '__main__':
  '''
  Для запуска 1 и 6 задачи над гарантировать наличие task_1_file && task_6_file в папке запуска
  '''
  # task1_reversed_blocks('task_1_file')
  # task2_string_flatter('')
  # task2_string_flatter('abcd aaabbc ))!kkkjqwebggds')
  # task3_is_correct_bracket('(){[()]}') #правильный вариант
  # task3_is_correct_bracket('{(([)])}') #неправильный вариант
  # task4_random_pass()
  # task5_is_palindrom("git t ii tt    i   gM") #лишняя с краю
  # task5_is_palindrom('abbccba') #лишняя по середине
  # task6_shredinger('task_6_file', 30)