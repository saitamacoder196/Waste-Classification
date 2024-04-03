CREATE TABLE detected_images (
    id SERIAL PRIMARY KEY,
    image_path TEXT NOT NULL,
    top_left_x INTEGER NOT NULL,
    top_left_y INTEGER NOT NULL,
    bottom_right_x INTEGER NOT NULL,
    bottom_right_y INTEGER NOT NULL,
    label TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_correct BOOLEAN NULL
)