#!/usr/bin/env run-cargo-script

// for read and write
// use std::fs::File;
// use std::io::{self, prelude::*, BufReader};
// use std::path::Path;

// for args
use std::env;

fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();

    let outfile_without_headers = &args[1];

    let mut reader1 = my_reader::BufReader::open(outfile_without_headers)?;
    let mut buffer1 = String::new();

    let mut reader2 = my_reader::BufReader::open(outfile_without_headers)?;
    let mut buffer2 = String::new();

    let mod_cutoff = 0.75;
    let un_cutoff = 0.25;
    let nucleosome_number = 40;

    let mut me_state_coop_me = 0;
    let mut me_state_coop_ac = 0;
    let mut me_state_rand_me = 0;
    let mut me_state_rand_ac = 0;

    let mut un_state_coop_me = 0;
    let mut un_state_coop_ac = 0;
    let mut un_state_rand_me = 0;
    let mut un_state_rand_ac = 0;

    let mut ac_state_coop_me = 0;
    let mut ac_state_coop_ac = 0;
    let mut ac_state_rand_me = 0;
    let mut ac_state_rand_ac = 0;

    // Flag for counting ac (1) and me (2) macrostates including the grey areas
    let mut macrostate = 0;

    let mut state_count_ac_including_grey = 0;
    let mut state_count_me_including_grey = 0;
    let mut state_count_ac_excluding_grey = 0;
    let mut state_count_me_excluding_grey = 0;
    let mut state_count_grey = 0;

    // Counter for current macrostate's length
    // grey area after current macrostate is added to it
    let mut state_length = 0;

    // Vecs which collect past macrostate lengths
    let mut me_vec = Vec::new();
    let mut ac_vec = Vec::new();

    // Skipping 1st line in 2nd buffer
    reader2.read_line(&mut buffer2);

    // Consumes the iterator, returns an (Optional) String
    while let Some(line2) = reader2.read_line(&mut buffer2) {
        let line1 = reader1.read_line(&mut buffer1);

        // println!(
        //     "{}",
        //     (&line1).as_ref().unwrap().as_deref().to_owned().unwrap()
        // );

        let mut me_count = 0;
        let mut un_count = 0;
        let mut ac_count = 0;

        let mut coop_me = 0;
        let mut coop_ac = 0;
        let mut rand_me = 0;
        let mut rand_ac = 0;

        let mut i = 0;
        for tup in (&line2)
            .as_ref()
            .unwrap()
            .clone()
            .strip_suffix("\n")
            .unwrap()
            .split_terminator(';')
        {
            // println!("'{}'", tup);
            let nucleosome_state = tup.split(':').next().unwrap().parse::<usize>().unwrap();
            match nucleosome_state {
                0 => un_count += 1,
                1 => ac_count += 1,
                2 => me_count += 1,
                _ => panic!(format!(
                    "0, 1 and 2 are valid options for states, not {}",
                    nucleosome_state
                )),
                // _ => println!(
                //     "0, 1 and 2 are valid options for states, not {}",
                //     nucleosome_state
                // ),
            }

            let nucleosomes_last_enzyme = (&line1)
                .as_ref()
                .unwrap()
                .as_deref()
                .to_owned()
                .unwrap()
                .split_terminator(';')
                .skip(i)
                .next()
                .unwrap();

            // println!("{}", nucleosomes_last_enzyme);

            let nucleosomes_last_enzyme_number: isize = nucleosomes_last_enzyme
                .splitn(2, ':')
                .skip(1)
                .next()
                .unwrap()
                .parse::<isize>()
                .unwrap();

            if nucleosomes_last_enzyme_number.clone() == -1 as isize {
                let nucleosome_enzyme = tup
                    .split(':')
                    .skip(1)
                    .next()
                    .unwrap()
                    .parse::<isize>()
                    .unwrap();
                match nucleosome_enzyme as isize {
                    -1 | 32 | 34 => (),
                    30 => rand_me += 1,
                    28 => rand_ac += 1,
                    0 | 2 | 4 | 6 | 8 | 10 | 12 => coop_ac += 1,
                    14 | 16 | 18 | 20 | 22 | 24 | 26 => coop_me += 1,
                    _ => panic!(format!(
                        "Invalid enzyme name {} in line2 \n{}",
                        nucleosome_enzyme,
                        line2.as_ref().unwrap().to_owned().to_string()
                    )),
                    // _ => println!(
                    //     "Invalid enzyme name {} from tup {} in line2 \n{}",
                    //     nucleosome_enzyme,
                    //     tup,
                    //     line2.as_ref().unwrap().to_owned().to_string()
                    // ),
                }
            }
            i += 1
        }

        if un_count >= (nucleosome_number as f32 * un_cutoff) as u8 {
            continue;
        } else if ac_count >= (nucleosome_number as f32 * mod_cutoff) as u8 {
            if macrostate == 2 {
                macrostate = 1;
                me_vec.push(state_length.to_string());
                // println!("Macrostate changed: \n{:?}", me_vec);
                state_length = 0;
            } else {
                macrostate = 1;
            }

            state_count_ac_excluding_grey += 1;

            ac_state_coop_me += coop_me;
            ac_state_coop_ac += coop_ac;
            ac_state_rand_me += rand_me;
            ac_state_rand_ac += rand_ac;
        } else if me_count >= (nucleosome_number as f32 * mod_cutoff) as u8 {
            if macrostate == 1 {
                macrostate = 2;
                ac_vec.push(state_length.to_string());
                // println!("Macrostate changed: \n{:?}", ac_vec);
                state_length = 0;
            } else {
                macrostate = 2;
            }
            state_count_me_excluding_grey += 1;

            me_state_coop_me += coop_me;
            me_state_coop_ac += coop_ac;
            me_state_rand_me += rand_me;
            me_state_rand_ac += rand_ac;
        } else {
            state_count_grey += 1;

            // TODO If grey area should not be contained in macrostates,
            // just add logic here (but 75 might then cause an issue)

            un_state_coop_me += coop_me;
            un_state_coop_ac += coop_ac;
            un_state_rand_me += rand_me;
            un_state_rand_ac += rand_ac;
        }

        state_length += 1;

        match macrostate {
            1 => state_count_ac_including_grey += 1,
            2 => state_count_me_including_grey += 1,
            _ => (),
        }
    }

    let me_vec_output = me_vec.iter().map(|s| &**s).collect::<Vec<&str>>().join(" ");

    let ac_vec_output = ac_vec.iter().map(|s| &**s).collect::<Vec<&str>>().join(" ");

    let output = format!(
        "\t\tCoopM\tCoopA\tRandM\tRandA\tcount(+Grey)\tcount(-Grey)
        Me\t{}\t{}\t{}\t{}\t{}\t{}
        Un\t{}\t{}\t{}\t{}\t/\t{}
        Ac\t{}\t{}\t{}\t{}\t{}\t{}",
        me_state_coop_me.to_string(),
        me_state_coop_ac.to_string(),
        me_state_rand_me.to_string(),
        me_state_rand_ac.to_string(),
        state_count_me_including_grey.to_string(),
        state_count_me_excluding_grey.to_string(),
        un_state_coop_me.to_string(),
        un_state_coop_ac.to_string(),
        un_state_rand_me.to_string(),
        un_state_rand_ac.to_string(),
        state_count_grey.to_string(),
        ac_state_coop_me.to_string(),
        ac_state_coop_ac.to_string(),
        ac_state_rand_me.to_string(),
        ac_state_rand_ac.to_string(),
        state_count_ac_including_grey.to_string(),
        state_count_ac_excluding_grey.to_string(),
    );

    println!(
        "
    {}

    ---

    {}
    {}",
        output, ac_vec_output, me_vec_output
    );

    Ok(())
}

mod my_reader {
    use std::{
        fs::File,
        io::{self, prelude::*},
    };

    pub struct BufReader {
        reader: io::BufReader<File>,
    }

    impl BufReader {
        pub fn open(path: impl AsRef<std::path::Path>) -> io::Result<Self> {
            let file = File::open(path)?;
            let reader = io::BufReader::new(file);

            Ok(Self { reader })
        }

        pub fn read_line<'buf>(
            &mut self,
            buffer: &'buf mut String,
        ) -> Option<io::Result<&'buf mut String>> {
            buffer.clear();

            self.reader
                .read_line(buffer)
                .map(|u| if u == 0 { None } else { Some(buffer) })
                .transpose()
        }
    }
}

// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
// fn read_lines<P>(histSimOutfile: P) -> io::Result<io::Lines<io::BufReader<File>>>
// where P: AsRef<Path>, {
//     let file = File::open(histSimOutfile)?;
//     Ok(io::BufReader::new(file).lines())
// }
