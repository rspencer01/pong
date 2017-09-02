import dent.Scene as Scene
import dent.RectangleObjects as RectangleObjects
from dent.RenderStage import RenderStage
import numpy as np
import dent.messaging as messaging
import logging

class MainScene(Scene.Scene):
  def __init__(self):
    super(MainScene, self).__init__()
    self.renderPipeline.stages.append(
        RenderStage(render_func = self.display, final_stage=True)
        )

    import dent.Texture
    dent.Texture.getWhiteTexture().load()

    self.ball = RectangleObjects.BlankImageObject()
    self.ball.width = 0.01
    self.ball.height = 0.01

    self.leftpaddle = RectangleObjects.BlankImageObject()
    self.leftpaddle.width = 0.01
    self.leftpaddle.height = 0.1
    self.leftpaddle.position[0] = 0.02

    self.rightpaddle = RectangleObjects.BlankImageObject()
    self.rightpaddle.width = 0.01
    self.rightpaddle.height = 0.1
    self.rightpaddle.position[0] = 0.98

    self.keys = set()

    self.reset()

    messaging.add_handler('timer', self.timer)
    messaging.add_handler('keyboard', self.key_down)
    messaging.add_handler('keyboard_up', self.key_up)


  def reset(self):
    self.ball.position = np.array([0.5, 0.5])
    self.ball.velocity = np.random.random_sample((2,))*2-1
    self.ball.velocity[1] /= 2
    self.ball.velocity /= np.linalg.norm(self.ball.velocity) * 3

  def display(self, **kwargs):
    self.ball.display()
    self.leftpaddle.display()
    self.rightpaddle.display()

  def key_down(self, key):
    self.keys.add(key)

  def key_up(self, key):
    if key in self.keys:
      self.keys.remove(key)

  def timer(self, fps):
    self.ball.position += self.ball.velocity * 1./fps
    if self.ball.position[1] < 0 or\
       self.ball.position[1] > 1:
      self.ball.velocity[1] *= -1
    if self.ball.position[0] < 0:
      logging.info("SCORE A!!!")
      self.reset()
    if self.ball.position[0] > 1:
      logging.info("SCORE B!!!")
      self.reset()

    if self.ball.position[0] < 0.03 and \
        abs(self.leftpaddle.position[1] - self.ball.position[1]) < 0.05:
      self.ball.velocity[0] *= -1
    if self.ball.position[0] > 0.97 and \
        abs(self.rightpaddle.position[1] - self.ball.position[1]) < 0.05:
      self.ball.velocity[0] *= -1

    if 'q' in self.keys:
      self.leftpaddle.position[1] = min(0.85, self.leftpaddle.position[1]+0.4/fps)
    if 'a' in self.keys:
      self.leftpaddle.position[1] = max(0.15, self.leftpaddle.position[1]-0.4/fps)
    if 'p' in self.keys:
      self.rightpaddle.position[1] = min(0.85, self.rightpaddle.position[1]+0.4/fps)
    if 'l' in self.keys:
      self.rightpaddle.position[1] = max(0.15, self.rightpaddle.position[1]-0.4/fps)
