import mdl
from display import *
from matrix import *
from draw import *

num_frames = 0
basename = ''
knobs = []
"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.

  jdyrlandweaver
  ==================== """
def first_pass( commands ):
    global num_frames
    global basename
    global knobs
    framesP = False
    basenameP = False
    varyP = False
    for command in commands:
        c = command[0]
        args = command[1:]
        if c == 'frames':
            num_frames = args[0]
            framesP = True           
        elif c == 'basename':
            basename = args[0]
            basenameP = True
        elif c == 'vary':
            varyP = True
    if varyP == True and framesP == False:
        print "Vary is used, but frames is not"
        exit()
    if framesP == True and basenameP == False:
        basename = "frame"
        print "Basename not found. Basename set as frame"
    
    pass


"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""
def second_pass( commands ):
    global num_frames
    global basename
    global knobs
    for x in range(num_frames):
        knobs.append({})
    for command in commands:
        c = command[0]
        args = command[1:]
        if c == 'vary':
            current = args[3]
            increment = (args[4] - current) / (args[2] - args[1] + 0.0)
            for x in range(args[1], args[2] + 1):
                knobs[x][args[0]] = current
                current += increment
    pass


def run(filename):
    global num_frames
    global basename
    global knobs
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return
    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    first_pass(commands)
    second_pass(commands)
    if num_frames > 0:
        for frame in range(num_frames):
            print "FRAME: " + str(frame)
            for symbol in symbols:
                symbols[symbol][1] = knobs[frame][symbol]
            for command in commands:                
                c = command[0]
                args = command[1:]

                if c == 'box':
                    add_box(tmp,
                            args[0], args[1], args[2],
                            args[3], args[4], args[5])
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, color)
                    tmp = []
                elif c == 'sphere':
                    add_sphere(tmp,
                               args[0], args[1], args[2], args[3], step)
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, color)
                    tmp = []
                elif c == 'torus':
                    add_torus(tmp,
                              args[0], args[1], args[2], args[3], args[4], step)
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, color)
                    tmp = []
                elif c == 'move':
                    adjust = 1
                    if args[3] != None:
                        adjust = symbols[args[3]][1]
                    tmp = make_translate(args[0] * adjust, args[1] * adjust, args[2] * adjust)
                    matrix_mult(stack[-1], tmp)
                    stack[-1] = [x[:] for x in tmp]
                    tmp = []
                elif c == 'scale':
                    if args[3] != None:
                        adjust = symbols[args[3]][1]                    
                    tmp = make_scale(args[0] * adjust, args[1] * adjust, args[2] * adjust)
                    matrix_mult(stack[-1], tmp)
                    stack[-1] = [x[:] for x in tmp]
                    tmp = []
                elif c == 'rotate':
                    if args[2] != None:
                        adjsut = symbols[args[2]][1]
                    theta = args[1] * adjust * (math.pi/180)
                    if args[0] == 'x':
                        tmp = make_rotX(theta)
                    elif args[0] == 'y':
                        tmp = make_rotY(theta)
                    else:
                        tmp = make_rotZ(theta)
                    matrix_mult( stack[-1], tmp )
                    stack[-1] = [ x[:] for x in tmp]
                    tmp = []
                elif c == 'push':
                    stack.append([x[:] for x in stack[-1]] )
                elif c == 'pop':
                    stack.pop()
                elif c == 'display':
                    display(screen)
                elif c == 'save':
                    save_extension(screen, args[0])
                print command
            print "Saving Frame:" + str(frame)
            save_extension(screen, "anim/" + basename + ("%03d" % frame) + ".png")
      

