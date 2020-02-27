import board
import busiPILo

from pillow import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
import speedtest
import math
import collections
import sys


def draw_nubers_n_hexes(down_speed, up_speed, ping, canvas, font):
    start_base = [92.0, 8.0]
    center = [start_base[0], start_base[1]]
    radius = [20.0, 10.0]
    canvas.polygon(generate_hexagon(center, radius), outline=255)
    canvas.text(get_text_start_for_hex(center, radius), down_speed, font=font, fill=1)
    center = [start_base[0], start_base[1]+radius[1]*math.sqrt(3)]
    radius = [20.0, 10.0]
    canvas.polygon(generate_hexagon(center, radius), outline=255)
    canvas.text(get_text_start_for_hex(center, radius), up_speed, font=font, fill=1)
    center = [start_base[0]+radius[0]+5, start_base[1]+radius[1]*math.sqrt(3)/2]
    radius = [10.0, 10.0]
    canvas.polygon(generate_hexagon(center, radius), outline=255)
    canvas.text(get_text_start_for_hex(center, radius), ping, font=font, fill=1)
    center = [start_base[0]+20+5, start_base[1]+radius[1]*math.sqrt(3)/2*3]
    canvas.polygon(generate_hexagon(center, radius), outline=255)
    center = [start_base[0]+20+5, start_base[1]+radius[1]*math.sqrt(3)/2*5]
    canvas.polygon(generate_hexagon(center, radius), outline=255)
    center = [start_base[0]-5, start_base[1]+radius[1]*math.sqrt(3)/2*5]
    canvas.polygon(generate_hexagon(center, radius), outline=255)


def draw_hex_load_indicator(on, canvas):
    start_base = [92.0, 8.0]
    radius = [10.0, 10.0]
    center = [start_base[0]+10, start_base[1]+radius[1]*math.sqrt(3)/2*4]
    if on:
        canvas.polygon(generate_hexagon(center, radius), outline=255, fill=1)
        radius = [9.0, 9.0]
        canvas.polygon(generate_hexagon(center, radius), outline=0, fill=1)
    else:
        canvas.polygon(generate_hexagon(center, radius), outline=255, fill=0)
        canvas.polygon(generate_hexagon(center, radius), outline=255)


def network_speed_test():
    servers = []
    # If you want to test against a specific server
    # servers = [1234]

    threads = None
    # If you want to use a single threaded test
    # threads = 1

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    print(f"{s.results.download}, {s.results.upload}, {s.results.ping}")
    return s


def generate_hexagon(center_point, size):
    y_offset = math.sqrt(3)/2*size[1]
    x_offset = 1/2*size[1]+size[0]-size[1]
    return [
                (center_point[0] - size[0], center_point[1]),
                (center_point[0] - x_offset, center_point[1] + y_offset),
                (center_point[0] + x_offset, center_point[1] + y_offset),
                (center_point[0] + size[0], center_point[1]),
                (center_point[0] + x_offset, center_point[1] - y_offset),
                (center_point[0] - x_offset, center_point[1] - y_offset),
            ]


def get_text_start_for_hex(center, radius):
    return [center[0]-radius[0]+radius[1]/2.0, center[1]-math.sqrt(3)/4*radius[1]]


def draw_network_graph(xy, hw, canvas, measurement_queue):
    # Draw left bracket
    canvas.line([(xy[0] + 0, xy[1] + 0), (xy[0] + 5, xy[1] + 0)], width=1, fill=1)
    canvas.line([(xy[0] + 0, xy[1] + 0), (xy[0] + 0, xy[1] + hw[0])], width=1, fill=1)
    canvas.line([(xy[0] + 0, xy[1] + hw[0]), (xy[0] + 5, xy[1] + hw[0])], width=1, fill=1)

    # Draw right bracket
    canvas.line([(xy[0] + hw[1], xy[1] + 0), (xy[0] + hw[1] - 5, xy[1] + 0)], width=1, fill=1)
    canvas.line([(xy[0] + hw[1], xy[1] + 0), (xy[0] + hw[1], xy[1] + hw[0])], width=1, fill=1)
    canvas.line([(xy[0] + hw[1], xy[1] + hw[0]), (xy[0] + hw[1] - 5, xy[1] + hw[0])], width=1, fill=1)

    # Get auto scale max
    scale_max = sys.float_info.epsilon
    for measurement in measurement_queue:
        scale_max = max(measurement.results.upload, scale_max)
        scale_max = max(measurement.results.download, scale_max)

    queue_draw_loc_x = xy[0] + hw[1] - 1
    for measurement in measurement_queue:

        if queue_draw_loc_x <= xy[0]:
            break

        if measurement.results.download > 0.0:
            canvas.point([queue_draw_loc_x, hw[0] - measurement.results.download/scale_max*hw[0]], fill=1)

        queue_draw_loc_x -= 1


# Entry point of the program
if __name__ == '__main__':
    EXECUTION_PERIOD_S = 60.0 * 30.0
    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the SSD1306 OLED class.
    disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

    # Network measumenet queue
    queue_size = 68
    speedtest_queue = collections.deque(queue_size*[speedtest.Speedtest()], queue_size)
    # Input pins:

    # Clear display.
    disp.fill(0)
    disp.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    fnt = ImageFont.truetype('Pillow/Tests/fonts/DejaVuSans.ttf', 10)

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    starttime = time.time() - EXECUTION_PERIOD_S
    print(starttime)
    while True:
        download_string = "----"
        upload_string = "----"
        ping_string = "--"

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        last_measurement_results = list(speedtest_queue)[0].results

        if last_measurement_results.download > 0.0:
            download_string = '{0:.2f}'.format(last_measurement_results.download / 1000000.0)

        if last_measurement_results.upload > 0.0:
            upload_string = '{0:.2f}'.format(last_measurement_results.upload / 1000000.0)

        if last_measurement_results.ping > 0.0:
            ping_string = '{0:.0f}'.format(last_measurement_results.ping)

        draw_nubers_n_hexes(download_string, upload_string, ping_string, draw, fnt)
        draw_network_graph([0, 0], [63, queue_size - 2], draw, speedtest_queue)
        draw_hex_load_indicator(False, draw)
        disp.image(image)
        disp.show()
        time_to_sleep = EXECUTION_PERIOD_S - min((time.time() - starttime), EXECUTION_PERIOD_S)
        time.sleep(time_to_sleep)
        starttime = time.time()
        draw_hex_load_indicator(True, draw)
        disp.image(image)
        disp.show()
        speedtest_queue.appendleft(network_speed_test())
