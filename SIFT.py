import numpy as np
import cv2

def make_scale_space(video_name, blur_levels, octave_levels):
    cap = cv2.VideoCapture(video_name);
    #octaves_set contains all octaves_set_single_frame
    octaves_set = [];
    frame_count = 0;
    while (cap.isOpened()):
        ret, frame = cap.read();
        if ret == False:
            break;

        frame_count = frame_count + 1;
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
        # making room for new octaves_set_single_frame
        # octaves_set.append([]);

        octaves_set_single_frame = [];

        k = 2;
        sigma = np.sqrt(2) / 2;

        for o_level in range(octave_levels):
            # adding new octave level
            octaves_set_single_frame.append([])

            for b_level in range(blur_levels):
                blurred_frame = cv2.GaussianBlur(frame, (5, 5), sigma);
                octaves_set_single_frame[o_level].append(blurred_frame);
                sigma = k * sigma;

            frame_dim = np.array(np.shape(frame));
            frame_dim = (frame_dim / 2).astype(np.uint32);
            # flipped frame_dim because in cv2.resize no: of columns come first
            frame = cv2.resize(frame, tuple(np.flip(frame_dim, 0)));

            # sigma starting point changes by a factor of sqrt(2) after every octave
            sigma = (np.sqrt(2) / 2) * (np.sqrt(2) ** (o_level + 1));

        # add current octaves_set_single_frame at the last location (which is initialized as empty sublist [])
        octaves_set.append(octaves_set_single_frame);

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break;

    cap.release();
    cv2.destroyAllWindows();
    return octaves_set

blur_levels = 5;
octave_levels = 4
octaves_set = make_scale_space('test_video.mp4', blur_levels, octave_levels);
LOG_set = [];
for frame_index in range(len(octaves_set)):
    LOG_single_frame = [];
    for o_level in range(octave_levels):
        LOG_single_frame.append([]);
        #blur_level - 1 = no: of subtraction operations performed
        for b_level in range(blur_levels - 1):
            #converted to np.int16 because subtractions answer can be negative
            LOG = (octaves_set[frame_index][o_level][b_level]).astype(np.int16) - \
                  (octaves_set[frame_index][o_level][b_level + 1]).astype(np.int16);
#            LOG = cv2.normalize(LOG, LOG, 0, 255, cv2.NORM_MINMAX, -1);
#            LOG = LOG.astype(np.uint8);
            LOG_single_frame[o_level].append(LOG);

    LOG_set.append(LOG_single_frame);

#for frame_index in range(len(octaves_set)):
#    cv2.imshow('LOG', LOG_set[frame_index][1][0]);
#    cv2.waitKey(25);
