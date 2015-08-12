import time
import log

from led import LEDMatrix
from led import LEDStrip
from led import LEDCircle
import colors

import threading

class animThread(threading.Thread):

    def __init__(self, anim, args):
        super(animThread, self).__init__()
        self.setDaemon(True)
        self._anim = anim
        self._args = args

    # def stopped(self):
    #     return self._anim._stopThread

    def run(self):
        log.logger.debug("Starting thread...")
        self._anim._run(**self._args)
        log.logger.debug("Thread Complete")

class BaseAnimation(object):
    def __init__(self, led):
        self._led = led
        self.animComplete = False
        self._step = 0
        self._timeRef = 0
        self._internalDelay = None
        self._threaded = False
        self._stopThread = False
        self._thread = None

    def _msTime(self):
        return time.time() * 1000.0

    def preRun(self):
        pass

    def step(self, amt = 1):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def stopThread(self, wait = False):
        if self._thread:
            self._stopThread = True
            if wait:
                self._thread.join()

    def stopped(self):
        if self._thread:
            return not self._thread.isAlive()
        else: 
            return True

    def _run(self, amt, fps, sleep, max_steps, untilComplete, max_cycles):
        """
        untilComplete makes it run until the animation signals it has completed a cycle
        max_cycles should be used with untilComplete to make it run for more than one cycle
        """
        self.preRun()

        #calculate sleep time base on desired Frames per Second
        if sleep == None and fps != None:
            sleep = int(1000 / fps)

        initSleep = sleep

        self._step = 0
        cur_step = 0
        cycle_count = 0
        self.animComplete = False

        while not self._stopThread and ((not untilComplete and (max_steps == 0 or cur_step < max_steps)) or (untilComplete and not self.animComplete)):
            self._timeRef = self._msTime()

            start = self._msTime()
            self.step(amt)
            mid = self._msTime()

            if initSleep:
                sleep = initSleep
            elif self._internalDelay:
                sleep = self._internalDelay

            self._led._frameGenTime = int(mid - start)
            self._led._frameTotalTime = sleep
            
            self._led.update()
            now = self._msTime()

            if self.animComplete and max_cycles > 0:
                if cycle_count < max_cycles - 1:
                    cycle_count += 1
                    self.animComplete = False

            stepTime = int(mid - start)
            if self._led._threadedUpdate:
                updateTime = int(self._led.lastThreadedUpdate())
                totalTime = updateTime
            else:
                updateTime = int(now - mid)
                totalTime = stepTime + updateTime

            if self._led._threadedUpdate:
                log.logger.debug("Frame: {}ms / Update Max: {}ms".format(stepTime, updateTime))
            else:
                log.logger.debug("{}ms/{}fps / Frame: {}ms / Update: {}ms".format(totalTime, int(1000 / max(totalTime,1)), stepTime, updateTime))

            if sleep:
                diff = (self._msTime() - self._timeRef)
                t = max(0, (sleep - diff) / 1000.0)
                if t == 0:
                    log.logger.warning("Frame-time of %dms set, but took %dms!" % (sleep, diff))
                time.sleep(t)
            cur_step += 1

    def run(self, amt = 1, fps=None, sleep=None, max_steps = 0, untilComplete = False, max_cycles = 0, threaded = False, joinThread = False):

        self._threaded = threaded
        self._stopThread = False

        if self._threaded:
            args =  locals()
            args.pop('self', None)
            args.pop('threaded', None)
            args.pop('joinThread', None)
            self._thread = animThread(self, args)
            self._thread.start()
            if joinThread:
                self._thread.join()
        else:
            self._run(amt, fps, sleep, max_steps, untilComplete, max_cycles)

class BaseStripAnim(BaseAnimation):
    def __init__(self, led, start = 0, end = -1):
        super(BaseStripAnim, self).__init__(led)

        if not isinstance(led, LEDStrip):
            raise RuntimeError("Must use LEDStrip with Strip Animations!")

        self._start = start
        self._end = end
        if self._start < 0:
            self._start = 0
        if self._end < 0 or self._end > self._led.lastIndex:
            self._end = self._led.lastIndex

        self._size = self._end - self._start + 1

class BaseMatrixAnim(BaseAnimation):
    def __init__(self, led, width=0, height=0, startX=0, startY=0):
        super(BaseMatrixAnim, self).__init__(led)
        if not isinstance(led, LEDMatrix):
            raise RuntimeError("Must use LEDMatrix with Matrix Animations!")

        if width == 0:
            self.width = led.width
        else:
            self.width = width

        if height == 0:
            self.height = led.height
        else:
            self.height = height

        self.startX = startX
        self.startY = startY

class BaseCircleAnim(BaseAnimation):
    def __init__(self, led):
        super(BaseCircleAnim, self).__init__(led)

        if not isinstance(led, LEDCircle):
            raise RuntimeError("Must use LEDCircle with Circle Animations!")

        self.rings = led.rings
        self.ringCount = led.ringCount
        self.lastRing = led.lastRing
        self.ringSteps = led.ringSteps

class StripChannelTest(BaseStripAnim):
    def __init__(self, led):
        super(StripChannelTest, self).__init__(led)
        self._internalDelay = 500
        self.colors =  [colors.Red, colors.Green, colors.Blue, colors.White]
  
    def step(self, amt = 1):
        
        self._led.set(0, colors.Red)
        self._led.set(1, colors.Green)
        self._led.set(2, colors.Green)
        self._led.set(3, colors.Blue)
        self._led.set(4, colors.Blue)
        self._led.set(5, colors.Blue)

        color =  self._step % 4
        self._led.fill(self.colors[color], 7, 9)

        self._step += 1

class MatrixChannelTest(BaseMatrixAnim):
    def __init__(self, led):
        super(MatrixChannelTest, self).__init__(led, 0, 0)
        self._internalDelay = 500
        self.colors =  [colors.Red, colors.Green, colors.Blue, colors.White]

    def step(self, amt = 1):
        
        self._led.drawLine(0, 0, 0, self.height - 1, colors.Red)
        self._led.drawLine(1, 0, 1, self.height - 1, colors.Green)
        self._led.drawLine(2, 0, 2, self.height - 1, colors.Green)
        self._led.drawLine(3, 0, 3, self.height - 1, colors.Blue)
        self._led.drawLine(4, 0, 4, self.height - 1, colors.Blue)
        self._led.drawLine(5, 0, 5, self.height - 1, colors.Blue)

        color =  self._step % 4
        self._led.fillRect(7, 0, 3, self.height, self.colors[color])

        self._step += 1

class MatrixCalibrationTest(BaseMatrixAnim):
    def __init__(self, led):
        super(MatrixCalibrationTest, self).__init__(led, 0, 0)
        self._internalDelay = 500
        self.colors = [colors.Red, colors.Green, colors.Green, colors.Blue, colors.Blue, colors.Blue]
       
    def step(self, amt = 1):
        self._led.all_off()
        i = self._step % self.width
        for x in range(i + 1):
            c = self.colors[x % len(self.colors)]
            self._led.drawLine(x, 0, x, i, c)

        self.animComplete = (i == (self.width-1))

        self._step += 1

