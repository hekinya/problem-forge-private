#import "lib.typ": contest-conf

#let language = sys.inputs.at("language")
#let data = json("/" + sys.inputs.at("hull-generated-json-path"))
#let display-name = data.display_name.at(language)
#let section(name) = read(language + "/" + name + ".typ")

// The template numbers problems for a contest booklet; this is a single problem.
#show "Problem A. ": none

#show: contest-conf.with(
  title: display-name,
  author: "",
  date: "",
  language: language,
  enable-titlepage: false,
  problems: (
    (
      problem: (
        display_name: display-name,
        format: "markup",
        samples: data.samples.map(sample => (
          input: sample.input.trim(),
          output: sample.outputs.output.trim(),
        )),
      ),
      statement: (
        description: section("description"),
        input: section("input"),
        output: section("output"),
      ),
    ),
  ),
)
