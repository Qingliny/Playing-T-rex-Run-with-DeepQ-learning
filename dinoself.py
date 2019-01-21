import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import time
from tqdm import tqdm
import pyautogui
import random
import cv2
from PIL import Image,ImageGrab
from collections import deque
import itertools
from scipy import stats
from copy import deepcopy

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

game_url = "chrome://dino"
chrome_driver_path = "/Users/qinglinyang/anaconda3/envs/RLhw1/bin/chromedriver-binary"

class DinoGame(object):
    def __init__(self,driver_path = chrome_driver_path,selenium = True):
        self.selenium = selenium
        if self.selenium:
            self.driver = webdriver.Chrome(driver_path)
            self.driver.get(game_url)
            self.body = self.driver.find_element_by_css_selector("body")


#implement operation 

    def click_screen(self):
        if not self.selenium:
            pyautogui.click(x=800,y = 300)


    def refresh_page(self):
        self.click_screen()
        pyautogui.hotkey('command', 'r')


    def move(self,action = "up"):
        if action is not None:
            if self.selenium:
                if action == "up":
                    self.body.send_keys(Keys.ARROW_UP)
                else:
                    self.body.send_keys(Keys.ARROW_DOWN)
            else:
                pyautogui.press(action)

#the policy

    def act(self,imgs,xs,score,policy = None,dino = None,**kwargs):
            """Action evaluation of the environment
            """

            # RANDOM POLICY
            if policy == "random":
                action = random.choice(["up","down",None])
                self.move(action)

            # HEURISTICS POLICY
            elif policy == "rules":
                th = 300 if "th" not in kwargs else kwargs["th"]
                th = max(th - score/100,150)
                if len(xs) > 0 and xs[0] < th:
                    self.move("up")

            # MACHINE LEARNING POLICY
            elif dino is not None:

                # Flat input method
                if "flat700" in dino.method:
                    xs = self.prepare_xs_vector(xs)
                    action,probas = dino.act(xs)
                    self.move(action)
                    return probas

                # Direct input method
                elif "direct" in dino.method:
                    n_obstacles = 2 if "n_obstacles" not in kwargs else kwargs["n_obstacles"]
                    xs = self.prepare_xs_direct(xs,n_obstacles = n_obstacles)
                    action,probas = dino.act(xs)
                    self.move(action)
                    return probas
            

            # NO POLICY
            else:
                pass






















