import settings as cfg


def bird_hit_bounds(bird):
    return bird.rect.top <= 0 or bird.rect.bottom >= cfg.PLAYABLE_HEIGHT


def bird_hit_pipe(bird, pipe):
    return pipe.collides_with(bird.rect)


def pipe_passed_bird(pipe):
    return pipe.top_rect.right < cfg.BIRD_X - cfg.BIRD_COLLISION_WIDTH // 2


def update_pipe_collisions_and_score(bird, pipes):
    score_gain = 0
    hit_pipe = False

    for pipe in pipes:
        if not pipe.scored and pipe_passed_bird(pipe):
            pipe.scored = True
            score_gain += 1

        if bird_hit_pipe(bird, pipe):
            hit_pipe = True

    return score_gain, hit_pipe


def bird_crashed(bird, pipes):
    if bird_hit_bounds(bird):
        return True

    return any(bird_hit_pipe(bird, pipe) for pipe in pipes)
