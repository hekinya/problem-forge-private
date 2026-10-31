#import "@preview/longops:0.2.1": pull-down
#import "@preview/pinit:0.2.2": absolute-place, pin, pinit

#let accent = rgb("#2f6fb0")
#let color-g = rgb("#d6e6f7")
#let color-q = rgb("#fdeeb9")
#let color-r = rgb("#cdeed6")
#let color-pad = luma(228)
#let color-error = rgb("#f6c4c0")
#let mono = "FiraCode Nerd Font"
#let bit-size = 5mm
#let arrow-coef = 118%

#let xor-bit(a, b) = if a == b { "0" } else { "1" }

/// Returns the quotient bits, the remainder bits, and every step of the division.
#let divide(dividend, g) = {
  let r = g.len() - 1
  let n = dividend.len() - r
  let x = dividend.clusters()
  let divisor = g.clusters()
  let quotient = ()
  let rows = ((kind: "x", bits: x, done: 0),)
  for i in range(n) {
    quotient.push(x.at(i))
    if x.at(i) == "1" {
      rows.push((kind: "g", at: i))
      for j in range(r + 1) {
        x.at(i + j) = xor-bit(x.at(i + j), divisor.at(j))
      }
      rows.push((kind: "x", bits: x, done: i + 1))
    }
  }
  (quotient: quotient, remainder: x.slice(n).join(), rows: rows)
}

#let digit(bit, fill: none, color: black) = grid.cell(
  fill: fill,
  text(fill: color, raw(bit)),
)

#let caption(body) = text(size: 0.85em, body)

#let lead(title) = [#v(0.6em)*#title．*]

/// Two transmissions of the same frame: one intact and one with a flipped bit.
#let flow(m, g, flipped) = {
  let r = g.len() - 1
  let frame = m + divide(m + "0" * r, g).remainder
  let wrong = frame
    .clusters()
    .enumerate()
    .map(((i, bit)) => if i == flipped { xor-bit(bit, "1") } else { bit })
    .join()
  let frame-fill(i) = if i >= m.len() { color-r }
  let wrong-fill(i) = if i == flipped { color-error } else { frame-fill(i) }
  let bits(s, fill: _ => none) = s
    .clusters()
    .enumerate()
    .map(((i, bit)) => digit(bit, fill: fill(i)))
  let head(span, body) = grid.cell(colspan: span, caption(body))
  let to = text(fill: luma(50%), $arrow.r$)
  let verdict(body) = grid.cell(
    align: left + horizon,
    inset: (left: 1em),
    caption(body),
  )
  let row(sent, received, fill, conclusion) = (
    ..bits(sent, fill: frame-fill),
    to,
    ..bits(received, fill: fill),
    to,
    ..bits(divide(received, g).remainder),
    verdict(conclusion),
  )
  let columns = frame.len() * 2 + r + 3

  align(center, grid(
    columns: (bit-size,) * frame.len()
      + (8mm,)
      + (bit-size,) * frame.len()
      + (8mm,)
      + (bit-size,) * r
      + (auto,),
    rows: (7mm, 6.5mm, 6.5mm, 6.5mm),
    align: center + horizon,
    grid.hline(y: 0, stroke: 1pt),
    grid.hline(y: 1, stroke: 0.4pt),
    grid.hline(y: 3, stroke: 1pt),
    head(frame.len(), [发送方]),
    [],
    head(frame.len(), [传输后]),
    [],
    head(r + 1, [接收方得到的余数]),
    ..row(frame, frame, frame-fill, [未发现错误]),
    ..row(frame, wrong, wrong-fill, [发现错误]),
    grid.cell(colspan: columns, caption[
      绿色是校验码，红色是传错的第 #(flipped + 1) 位
    ]),
  ))
}

#let xor-figure = {
  let rule(a, b) = (
    digit(a),
    $xor$,
    digit(b),
    $=$,
    digit(xor-bit(a, b), fill: color-q),
  )
  let rules = grid(
    columns: (bit-size,) * 5 + (6mm,) + (bit-size,) * 5,
    rows: bit-size,
    row-gutter: 1.5mm,
    align: center + horizon,
    ..rule("0", "0"),
    [],
    ..rule("0", "1"),
    ..rule("1", "0"),
    [],
    ..rule("1", "1"),
  )

  let top = "1100".clusters()
  let bottom = "1010".clusters()
  let example = grid(
    columns: (bit-size,) * 5,
    rows: bit-size,
    align: center + horizon,
    grid.hline(y: 2, start: 1),
    [],
    ..top.map(digit),
    $xor$,
    ..bottom.map(digit),
    [],
    ..range(4).map(i => digit(
      xor-bit(top.at(i), bottom.at(i)),
      fill: color-q,
    )),
  )

  align(center, grid(
    columns: (auto, auto),
    column-gutter: 14mm,
    align: horizon,
    rules, example,
  ))
}

/// Long division on a grid. Longops draws the pull-down arrows, but its own
/// `division` subtracts with borrows, so the steps here come from `divide`.
#let ladder(m, g) = {
  let n = m.len()
  let r = g.len() - 1
  let result = divide(m + "0" * r, g)
  let divisor = g.clusters()
  let dividend = result.rows.first().bits
  let steps = result.rows.filter(row => row.kind == "g").map(row => row.at)
  let works = result.rows.filter(row => row.kind == "x").slice(1)
  let offset = r + 1
  let notes = offset + n + r
  let row-count = 2 + 2 * steps.len()

  let next(k) = if k + 1 < steps.len() { steps.at(k + 1) }
  let last-shown(k) = if next(k) == none { n + r - 1 } else { next(k) + r }
  let note(body) = grid.cell(
    align: left + horizon,
    inset: (left: 1em),
    caption(body),
  )
  let skipped(row, stop) = range(row.done, n)
    .filter(j => (stop == none or j < stop) and row.bits.at(j) == "0")
    .map(j => [第 #(j + 1) 位是 `0`：跳过])

  let cells = (:)
  let covered = ()
  let put(cells, y, x, cell) = {
    cells.insert(str(y) + "," + str(x), cell)
    cells
  }

  for (i, bit) in result.quotient.enumerate() {
    cells = put(cells, 0, offset + i, digit(bit, fill: color-q))
  }
  cells = put(cells, 0, notes, note[黄色是商 $Q$])

  for (j, bit) in divisor.enumerate() {
    cells = put(cells, 1, j, digit(bit, fill: color-g))
  }
  for (j, bit) in dividend.enumerate() {
    let fill = if j >= n { color-pad }
    cells = put(cells, 1, offset + j, digit(bit, fill: fill))
  }
  let first = steps.at(0, default: none)
  let intro = ([灰色是补的 #r 个 `0`],)
  intro += skipped(result.rows.first(), first)
  cells = put(cells, 1, notes, note(intro.join[；]))

  let lines = (
    grid.hline(y: 1, start: offset, end: notes),
    grid.vline(x: offset, start: 1, end: 2),
  )

  for (k, i) in steps.enumerate() {
    let y = 2 + 2 * k
    cells = put(cells, y, offset + i - 1, grid.cell($xor$))
    for (j, bit) in divisor.enumerate() {
      cells = put(cells, y, offset + i + j, digit(bit, fill: color-g))
    }
    cells = put(cells, y, notes, note[第 #(i + 1) 位是 `1`：对齐 $G$，做异或])
    lines.push(grid.hline(
      y: y + 1,
      start: offset + i,
      end: offset + i + r + 1,
    ))

    let stop = next(k)
    let done = k == steps.len() - 1
    for j in range(i, last-shown(k) + 1) {
      let bit = works.at(k).bits.at(j)
      let cell = if done and j >= n {
        digit(bit, fill: color-r)
      } else if j < (if stop == none { n } else { stop }) {
        digit(bit, color: luma(165))
      } else {
        digit(bit)
      }
      cells = put(cells, y + 1, offset + j, cell)
    }
    let remarks = skipped(works.at(k), stop)
    if done { remarks.push[绿色是余数 $R$] }
    if remarks.len() > 0 {
      cells = put(cells, y + 1, notes, note(remarks.join[；]))
    }
  }

  // A digit is pulled down to the first work row that shows it.
  if first != none {
    for j in range(first + r + 1, n + r) {
      let k = range(steps.len()).find(k => last-shown(k) >= j)
      let span = 2 * k + 1
      cells = put(cells, 2, offset + j, pull-down(span, coef: arrow-coef))
      covered += range(3, 2 + span).map(y => str(y) + "," + str(offset + j))
    }
  }

  let body = ()
  for y in range(row-count) {
    for x in range(notes + 1) {
      let key = str(y) + "," + str(x)
      if key in cells {
        body.push(cells.at(key))
      } else if key not in covered {
        body.push([])
      }
    }
  }

  align(center, grid(
    columns: (bit-size,) * notes + (auto,),
    rows: bit-size,
    align: center + horizon,
    ..lines,
    ..body,
  ))
}

/// One line of literal input or output, with every field labeled below it.
#let fields(id, prefix, ..parts) = {
  let names = parts.pos().enumerate().map(((i, _)) => id + "-" + str(i))
  let text-line = parts
    .pos()
    .enumerate()
    .map(((i, part)) => [#pin(names.at(i) + "-a")#text(font: mono)[#part.at(
        0,
      )]#pin(names.at(i) + "-b")])
    .join(h(1em))
  let marks = parts
    .pos()
    .enumerate()
    .map(((i, part)) => pinit(
      names.at(i) + "-a",
      names.at(i) + "-b",
      callback: (a, b) => {
        absolute-place(dx: a.x, dy: a.y + 3.5pt, line(
          length: b.x - a.x,
          stroke: 1pt + accent,
        ))
        absolute-place(
          dx: (a.x + b.x) / 2 - 2cm,
          dy: a.y + 5pt,
          box(width: 4cm, align(center, text(
            size: 0.85em,
            fill: accent,
            part.at(1),
          ))),
        )
      },
    ))
    .join()
  [#align(center)[#prefix#h(1em)#text-line]#marks#v(1.3em)]
}
