#![feature(generic_const_exprs)]

use std::ops::Neg;

const SAMPLE_FREQ: usize = 16000;

const ANZ_HIST_KAN: usize = 4;
const HIST_CLASS_1: usize = SAMPLE_FREQ / 1000;
const HIST_CLASS_2: usize = SAMPLE_FREQ / 100;
const HIST_CLASS_3: usize = SAMPLE_FREQ / 10;
const HIST_CLASS_1_INC: f64 = 1.0;
const HIST_CLASS_2_INC: f64 = 1.0;
const HIST_CLASS_3_INC: f64 = 1.0;
const HIST_CLASS_4_INC: f64 = 1.0;

enum Status {
    OK = 0,
    ERROR = -1,
    NOOP = 1,
}

fn zero_crossings<T: Ord + Neg<Output = T> + Copy>(samples: &[T], threshold: T) -> Vec<usize> {
    let current_state = 0; // 1: above threshold, -1: below threshold
    let mut crossings = Vec::new();

    for (i, val) in samples.iter().enumerate() {
        if *val > threshold {
            if current_state == -1 {
                crossings.push(i);
            }
        }
        if *val < -threshold {
            if current_state == -1 {
                crossings.push(i);
            }
        }
    }
    return crossings;
}

fn differentiate_array<T: std::ops::Sub<Output = T> + Copy>(array: &[T]) -> Box<[T]> {
    array.windows(2).map(|w: &[T]| w[1] - w[0]).collect()
}

fn crossing_histogram(crossings: Vec<usize>) -> [f64; ANZ_HIST_KAN] {
    let mut hist_buf = [0f64; ANZ_HIST_KAN];
    for w in crossings.windows(2) {
        let distance = w[1] - w[0];

        if distance < HIST_CLASS_1 {
            hist_buf[0] += HIST_CLASS_1_INC;
        } else if distance < HIST_CLASS_2 {
            hist_buf[1] += HIST_CLASS_2_INC;
        } else if distance < HIST_CLASS_3 {
            hist_buf[2] += HIST_CLASS_3_INC;
        } else {
            hist_buf[3] += HIST_CLASS_4_INC;
        }
    }
    hist_buf
}

const ENERGY_BLUR: usize = SAMPLE_FREQ / 100; // UNSURE WHAT TO USE
const ENERGY_RELATIVE_THRESHOLD: f64 = 0.25; // UNSURE WHAT TO USE
const ENERGY_DURATION_THRESHOLD: usize = SAMPLE_FREQ / 10; // UNSURE WHAT TO USE
fn signal_detekt(samples: &mut [i16]) -> Option<&[i16]> {
    // CALCULATE ENERGY
    let energy: Box<[i16]> = samples
        .iter()
        .enumerate()
        .map(|(i, _)| {
            let start_idx: usize = if i < ENERGY_BLUR { 0 } else { i - ENERGY_BLUR };
            let window_len: usize = if i < ENERGY_BLUR { i + 1 } else { ENERGY_BLUR };
            samples[start_idx..start_idx + window_len]
                .iter()
                .map(|x| x.pow(2))
                .sum()
        })
        .collect();

    let energy_threshold = (*energy.iter().max()? as f64 * ENERGY_RELATIVE_THRESHOLD) as i16;

    let mut signal: &mut [i16];
    // SIGNAL DETECTION
    for (i, sample) in samples.iter().enumerate() {
        if *sample > energy_threshold {
            for (offset, right_sample) in samples[i..].iter().enumerate() {
                if *right_sample < energy_threshold {
                    signal = &mut samples[i..i + offset];
                    break;
                }
            }
        }
        if signal.len() > ENERGY_DURATION_THRESHOLD {
            break;
        }
    }
    if signal.len() < ENERGY_DURATION_THRESHOLD {
        return None;
    }

    // REMOVE DC PART
    let dc_level = samples.iter().sum::<i16>() / samples.len() as i16;
    signal.iter_mut().map(|val| *val -= dc_level);

    Some(signal)
}

const NOISE_THRESHOLD: u16 = 50; // UNSURE WHAT TO USE
// Status ndg_dichte(short *feld_ptr, unsigned int anzahl_atw, float *dichte_ori, float *dichte_diff)
// {
//     if (feld_ptr == NULL || dichte_ori == NULL || dichte_diff == NULL)
//         return ERROR;

//     // SETUP
//     size_t *crossings_buf = malloc(anzahl_atw * sizeof(size_t));
//     if (crossings_buf == NULL)
//         return ERROR;
//     size_t crossings;

//     // CALC ORIGINAL
//     zero_crossings(feld_ptr, anzahl_atw, NOISE_THRESHOLD, crossings_buf, &crossings);

//     *dichte_ori = (float)crossings / (float)anzahl_atw;

//     // CALC DIFFERNTIATED

//     size_t diff_buf_len = anzahl_atw - 1;
//     short *diff_buf = malloc(diff_buf_len * sizeof(short));
//     if (diff_buf == NULL)
//     {
//         free(crossings_buf);
//         return ERROR;
//     }
//     differentiate_array(feld_ptr, anzahl_atw, diff_buf);

//     zero_crossings(diff_buf, diff_buf_len, NOISE_THRESHOLD, crossings_buf, &crossings);

//     *dichte_diff = (float)crossings / (float)diff_buf_len;

//     free(diff_buf);
//     free(crossings_buf);

//     return OK;
// }

// Status ndg_histogramm(short *feld_ptr, unsigned int anzahl_atw, float *hist_ori, float *hist_diff)
// {
//     if (feld_ptr == NULL || hist_ori == NULL || hist_diff == NULL)
//         return ERROR;

//     // SETUP
//     size_t *crossings_buf = malloc(anzahl_atw * sizeof(size_t));
//     if (crossings_buf == NULL)
//         return ERROR;
//     size_t crossings;

//     // ZERO OUT IN-HIST-BUFS
//     for (size_t i = 0; i < ANZ_HIST_KAN; i++)
//     {
//         hist_ori[i] = 0;
//         hist_diff[i] = 0;
//     }

//     // CALC ORI
//     zero_crossings(feld_ptr, anzahl_atw, NOISE_THRESHOLD, crossings_buf, &crossings);
//     crossing_histogram(crossings_buf, crossings, hist_ori);

//     // CALC DIFF
//     size_t diff_buf_len = anzahl_atw - 1;
//     short *diff_buf = malloc(diff_buf_len * sizeof(short));
//     if (diff_buf == NULL)
//     {
//         free(crossings_buf);
//         return ERROR;
//     }

//     differentiate_array(feld_ptr, anzahl_atw, diff_buf);
//     zero_crossings(diff_buf, diff_buf_len, NOISE_THRESHOLD, crossings_buf, &crossings);
//     crossing_histogram(crossings_buf, crossings, hist_diff);

//     // CLEANUP
//     free(crossings_buf);
//     free(diff_buf);
//     return OK;
// }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
