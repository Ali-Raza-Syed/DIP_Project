import numpy as np
import cv2

def make_scale_space(video_name):
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

        blur_levels = 5;
        octave_levels = 4;

        # making room for new octaves_set_single_frame
        # octaves_set.append([]);

        octaves_set_single_frame = [];

        k = 2;
        sigma = 1;

        for o_level in range(octave_levels):
            # adding new octave level
            octaves_set_single_frame.append([])

            for b_level in range(blur_levels):
                blurred_frame = cv2.GaussianBlur(frame, (5, 5), sigma);
                octaves_set_single_frame[o_level].append(blurred_frame);
                if b_level == 0 and o_level == 0:
                    cv2.imshow('Level 1', blurred_frame);
                if b_level == 4 and o_level == 1:
                    cv2.imshow('Level 4', blurred_frame);
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

video_name = 'test_video.mp4';
octaves_set = make_scale_space(video_name);
