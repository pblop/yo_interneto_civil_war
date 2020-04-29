from PIL import Image, ImageDraw, ImageFont
import math

def get_widths(columns, sizes, participants_by_column, PARTICIPANTS_PER_COLUMN, COLUMN_MARGIN):
  # Calculate the last column on its own
  columns_width = []
  for col_number in range(0, columns):
    column_length = len(participants_by_column[col_number])
    text_widths = []
    for participant_in_column_number in range(0, column_length):
      idx= col_number*PARTICIPANTS_PER_COLUMN + participant_in_column_number
      w, h = sizes[idx]
      text_widths.append(w)

    column_width = max(text_widths)
    if col_number == (columns - 1):
      # Last column
      last_column_width = column_width
    else:
      columns_width.append(round(column_width + column_width*COLUMN_MARGIN))


  max_column_width = max(columns_width)
  image_width = max_column_width*(columns-1) + last_column_width
  return image_width, max_column_width

def apply_margins_to_image(height_margin, width_margin, height, width):
  height += + height_margin*2 # *2 means top and bottom margins
  height = round(height)
  width += width_margin*2 # *2 means left and right margins
  width = round(width)


  return height, width

def draw_names(height, width, height_margin, width_margin, columns, max_name_height, max_column_width, participants_by_column, font):
  # Drawing
  img = Image.new('RGB', (width, height), (255, 255, 255))
  d = ImageDraw.Draw(img)

  h_index = height_margin
  w_index = width_margin
  for column_number in range(0, columns):
    col_width = max_column_width
    col_participants = participants_by_column[column_number]

    for participant in col_participants:
      d.text((w_index, h_index), participant.name, fill=(0, 0, 0), font=font)

      if not participant.isalive():
        w, h = font.getsize(participant.name)
        middle_h = h_index + round(max_name_height/2)
        d.line([(w_index, middle_h), (w_index+w, middle_h)], fill=(255, 0, 0), width=5)
      
      h_index += max_name_height
    
    w_index += col_width
    h_index = height_margin

  return img

def draw_participants(participants, VERT_AND_HTAL_MARGIN = 0.1, COLUMN_MARGIN = 0.2, PARTICIPANTS_PER_COLUMN = 30):
  columns = math.ceil(len(participants)/PARTICIPANTS_PER_COLUMN)
  participants_by_column = [participants[x:x+PARTICIPANTS_PER_COLUMN] for x in range(0, len(participants), PARTICIPANTS_PER_COLUMN)]

  font = ImageFont.truetype('arial.ttf', 48)
  sizes = [font.getsize(participant.name) for participant in participants]
  max_name_height = max(h for w, h in sizes)

  # Calculating height
  # Image height is the same as column height
  image_height = round(max_name_height * PARTICIPANTS_PER_COLUMN)
  image_margin = image_height*VERT_AND_HTAL_MARGIN

  # image_height_margin = image_height*VERT_MARGIN
  image_height_margin = image_margin

  # Calculate widths
  image_width, max_column_width = get_widths(columns, sizes, participants_by_column, PARTICIPANTS_PER_COLUMN, COLUMN_MARGIN)
  # image_width_margin = image_width*HTAL_MARGIN
  image_width_margin = image_margin
  
  image_height, image_width = apply_margins_to_image(image_height_margin, image_width_margin, image_height, image_width)

  img = draw_names(image_height, image_width, image_height_margin, image_width_margin, columns, max_name_height, max_column_width, participants_by_column, font)
  return img

if __name__ == '__main__':
  def get_participants():
    participants = []
    with open('participants.txt', 'r') as f:
      while True:
        line = f.readline()
        if line == '':
          break
        name = line.replace('\n', '')
        participants.append(Participant(name))
    return participants

  def set_dead_participants(participants):
    with open('dead.txt', 'r') as f:
      while True:
        line = f.readline()
        if line == '':
          break
        name = line.replace('\n', '')
        participant = [participant for participant in participants if participant.name == name][0]
        participant.alive = False

  class Participant:
    def __init__(self, name):
      self.name = name
      self.alive = True

    def isalive(self):
      return self.alive

  participants = get_participants()
  set_dead_participants(participants)
  draw_participants(participants).save('participants.png')
