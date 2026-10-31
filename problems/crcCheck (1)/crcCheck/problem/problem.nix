{
  hull,
  lib,
  config,
  cplib,
  pkgs,
  ...
}:
{
  name = "crcCheck";

  displayName.zh = "循环冗余校验";

  tickLimit = 1000 * 10000000;
  memoryLimit = 1024 * 1024 * 1024;

  authoringIncludes = [
    cplib
    ./authoring-include
  ];

  generators = {
    rand.src = ./generator/rand.23.cpp;
    exhaustive.src = ./generator/exhaustive.23.cpp;
  };

  validator = {
    src = ./validator.23.cpp;
    tests =
      let
        zeros = n: lib.strings.replicate n "0";
        valid = { status, ... }: status == "valid";
        invalid = { status, ... }: status == "invalid";
      in
      {
        minimal = {
          inputFile = builtins.toFile "minimal.in" "1\n0 10\n";
          prediction = valid;
        };
        maxLength = {
          inputFile = builtins.toFile "maxLength.in" "1\n${zeros 5000} 1${zeros 4999}\n";
          prediction = valid;
        };
        tooManyCases = {
          inputFile = builtins.toFile "tooManyCases.in" ("1001\n" + lib.strings.replicate 1001 "0 10\n");
          prediction = invalid;
        };
        sumMTooLarge = {
          inputFile = builtins.toFile "sumMTooLarge.in" "2\n${zeros 2500} 11\n${zeros 2501} 11\n";
          prediction = invalid;
        };
        sumGTooLarge = {
          inputFile = builtins.toFile "sumGTooLarge.in" "2\n0 1${zeros 2499}\n0 1${zeros 2500}\n";
          prediction = invalid;
        };
        gLeadingZero = {
          inputFile = builtins.toFile "gLeadingZero.in" "1\n1 011\n";
          prediction = invalid;
        };
        gTooShort = {
          inputFile = builtins.toFile "gTooShort.in" "1\n1 1\n";
          prediction = invalid;
        };
        badCharacter = {
          inputFile = builtins.toFile "badCharacter.in" "1\n102 11\n";
          prediction = invalid;
        };
        noEoln = {
          inputFile = builtins.toFile "noEoln.in" "1\n1 11";
          prediction = invalid;
        };
        trailingLine = {
          inputFile = builtins.toFile "trailingLine.in" "1\n1 11\n1 11\n";
          prediction = invalid;
        };
      };
  };

  checker = {
    src = ./checker.23.cpp;
    tests =
      let
        input = builtins.toFile "checker.in" "2\n101001 1101\n0011 101\n";
        accepted = { status, ... }: status == "accepted";
        wrong = { status, ... }: status == "wrong_answer";
      in
      {
        correct = {
          inputFile = input;
          outputFile = builtins.toFile "correct.out" "110101 001\n11 11\n";
          prediction = accepted;
        };
        quotientLeadingZero = {
          inputFile = input;
          outputFile = builtins.toFile "quotientLeadingZero.out" "110101 001\n0011 11\n";
          prediction = wrong;
        };
        remainderShort = {
          inputFile = input;
          outputFile = builtins.toFile "remainderShort.out" "110101 1\n11 11\n";
          prediction = wrong;
        };
        missingToken = {
          inputFile = input;
          outputFile = builtins.toFile "missingToken.out" "110101 001\n11\n";
          prediction = wrong;
        };
        extraToken = {
          inputFile = input;
          outputFile = builtins.toFile "extraToken.out" "110101 001\n11 11\n1\n";
          prediction = wrong;
        };
      };
  };

  traits = { };

  testCases =
    let
      defaults = {
        t = 1;
        n = 5000;
        g = 5000;
        headN = null;
        headG = null;
        mKind = "random";
        density = 50;
        zeros = 0;
        remBits = 0;
        gKind = "random";
        gDensity = 50;
        gOdd = false;
        salt = 0;
      };
      rand =
        spec:
        let
          s = defaults // spec;
        in
        {
          generator = "rand";
          arguments = [
            "--t=${toString s.t}"
            "--n=${toString s.n}"
            "--g=${toString s.g}"
            "--head-n=${toString (if s.headN == null then s.n else s.headN)}"
            "--head-g=${toString (if s.headG == null then s.g else s.headG)}"
            "--m-kind=${s.mKind}"
            "--density=${toString s.density}"
            "--zeros=${toString s.zeros}"
            "--rem-bits=${toString s.remBits}"
            "--g-kind=${s.gKind}"
            "--g-density=${toString s.gDensity}"
          ]
          ++ lib.optional s.gOdd "--g-odd"
          ++ [ "--salt=${toString s.salt}" ];
        };
    in
    {
      sample1 = {
        inputFile = ./data/sample-1.in;
        groups = [ "sample" ];
      };

      exhaustive = {
        generator = "exhaustive";
        arguments = [
          "--max-m=4"
          "--max-g=5"
        ];
      };

      # Many small cases.
      minCases = rand {
        t = 1000;
        n = 1;
        g = 2;
      };
      smallShortG = rand {
        t = 500;
        n = 8;
        g = 3;
      };
      smallShortM = rand {
        t = 500;
        n = 2;
        g = 8;
      };
      smallBalanced = rand {
        t = 100;
        n = 14;
        g = 8;
      };
      smallSparseM = rand {
        t = 300;
        n = 10;
        g = 6;
        density = 15;
        gDensity = 15;
      };

      # Lengths around the width of a 64-bit integer.
      around64 = rand {
        t = 70;
        n = 60;
        g = 64;
      };
      over64G = rand {
        t = 70;
        n = 40;
        g = 65;
      };
      over64M = rand {
        t = 30;
        n = 120;
        g = 40;
      };
      mediumBalanced = rand {
        t = 10;
        n = 500;
        g = 500;
      };

      # Maximum work and the extreme length ratios.
      maxRandom = rand { };
      maxDenseM = rand {
        density = 90;
        salt = 1;
      };
      maxSparseG = rand {
        gDensity = 5;
        salt = 2;
      };
      maxAllOnes = rand {
        density = 100;
        gDensity = 100;
      };
      maxAlternating = rand {
        mKind = "alternating";
        salt = 3;
      };
      maxQuotientOnes = rand {
        density = 100;
        gDensity = 0;
      };
      longMShortG11 = rand {
        g = 2;
        gDensity = 100;
      };
      longMShortG10 = rand {
        g = 2;
        gDensity = 0;
      };
      longMShortG3 = rand {
        g = 3;
        salt = 4;
      };
      shortMLongG = rand {
        n = 1;
        density = 100;
      };
      shortMLongG2 = rand {
        n = 2;
        density = 100;
        salt = 5;
      };

      # Quotient boundaries.
      allZeroM = rand { density = 0; };
      leadingZeroM = rand {
        zeros = 4990;
        salt = 6;
      };
      halfLeadingZeroM = rand {
        zeros = 2500;
        salt = 7;
      };
      mixedZeroM = rand {
        t = 100;
        n = 20;
        g = 10;
        zeros = 18;
      };

      # Special generator strings.
      gEndsOnes = rand {
        gDensity = 0;
        gOdd = true;
      };
      gPowerOfTwo = rand {
        g = 2500;
        gDensity = 0;
      };
      gLowZeros = rand {
        t = 50;
        n = 40;
        g = 30;
        gDensity = 0;
        salt = 8;
      };
      crc8 = rand {
        gKind = "crc8";
        g = 9;
      };
      crc16 = rand {
        gKind = "crc16";
        g = 17;
      };
      crc32 = rand {
        gKind = "crc32";
        g = 33;
      };
      crc32Many = rand {
        t = 100;
        n = 50;
        g = 33;
        gKind = "crc32";
      };

      # Remainders with a long run of leading zeros.
      remainderZero = rand {
        mKind = "tail";
        g = 2500;
        gOdd = true;
      };
      remainderZeroMany = rand {
        t = 20;
        n = 200;
        g = 100;
        mKind = "tail";
        gOdd = true;
      };
      remainderOneBit = rand {
        mKind = "tail";
        g = 2000;
        gOdd = true;
        remBits = 1;
      };
      remainderFewBits = rand {
        t = 10;
        n = 400;
        g = 300;
        mKind = "tail";
        gOdd = true;
        remBits = 8;
      };

      # One big case together with many minimum cases.
      bigAndSmall = rand {
        t = 1000;
        n = 1;
        g = 2;
        headN = 4001;
        headG = 3001;
      };
    };

  subtasks = [ { fullScore = 1.0; } ];

  solutions =
    let
      ac = { score, ... }: score == 1.0;
      wa = { statuses, ... }: builtins.elem "wrong_answer" statuses;
      tleOrAc =
        { statuses, ... }: builtins.all (s: s == "accepted" || s == "time_limit_exceeded") statuses;
      wrongSolution = src: {
        inherit src;
        subtaskPredictions."0" = wa;
      };
    in
    {
      std = {
        src = ./solution/std.17.cpp;
        mainCorrectSolution = true;
        subtaskPredictions."0" = ac;
      };
      bruteForce = {
        src = ./solution/bf.17.cpp;
        subtaskPredictions."0" = tleOrAc;
      };
      slowString = {
        src = ./solution/slow_string.17.cpp;
        subtaskPredictions."0" = ac;
      };
      waUll = wrongSolution ./solution/wa_ull.17.cpp;
      waNoAppend = wrongSolution ./solution/wa_no_append.17.cpp;
      waNoPad = wrongSolution ./solution/wa_no_pad.17.cpp;
      waQuotientZeros = wrongSolution ./solution/wa_quotient_zeros.17.cpp;
      waOrdinaryDiv = wrongSolution ./solution/wa_ordinary_div.17.cpp;
    };

  documents =
    let
      languages = [ "zh" ];
      olympInTypst = pkgs.fetchFromGitHub {
        owner = "lihaoze123";
        repo = "olymp-in-typst";
        rev = "3c82fe3dd4ce2540dec6bffcc7ce25f1f20947e6";
        hash = "sha256-grbZJtb303GZDUJ9V0hGLSRod5wWA8rto+1e3iTUdpw=";
      };
      foundertypeFont =
        name: hash:
        pkgs.fetchurl {
          url = "https://cdn1.foundertype.com/Public/Uploads/ttf/${name}";
          inherit hash;
          curlOptsList = [
            "--user-agent"
            "Mozilla/5.0"
          ];
        };
      foundertypeFonts = pkgs.linkFarm "foundertype-fonts" [
        {
          name = "FZSSK.TTF";
          path = foundertypeFont "FZSSK.TTF" "sha256-AP2/tDOq9MAN0Ct5MZu/6U/8o5nbob6eZFXku2UOAnM=";
        }
        {
          name = "FZHTK.TTF";
          path = foundertypeFont "FZHTK.TTF" "sha256-W+Y9vIZPBLAS+D21Oy4OpKLHAxHEpCzDPGIGrpzUfvA=";
        }
        {
          name = "FZXBSK.TTF";
          path = foundertypeFont "FZXBSK.TTF" "sha256-puTh7oh4uCS062bcWOJe0lWZLvOskBJkuERKW8WjACk=";
        }
      ];
      statementSrc = pkgs.runCommandLocal "hull-olympStatement-${config.name}" { } ''
        mkdir $out
        cp -r ${./document/statement}/. $out/
        cp ${olympInTypst}/lib.typ $out/lib.typ
      '';
      mkStatement = language: {
        "statement.${language}.pdf" = {
          path = hull.document.mkProblemTypstDocument config {
            src = statementSrc;
            inputs = { inherit language; };
            typstPackages = [
              {
                name = "numbly";
                version = "0.1.0";
                hash = "sha256-j3kolGf2gAJiXGymYpmtWiOJbtOvjQz8xxVjxKmjDQw=";
              }
              {
                name = "cmarker";
                version = "0.1.6";
                hash = "sha256-Rwbp3xfvtxX/0jEAaqQF5Ekg0RPe/bp9ZdqWdcrtoNM=";
              }
              {
                name = "mitex";
                version = "0.2.6";
                hash = "sha256-bSWz2OXgFasfFhGEzjzA/wtvafL9bjfqs8r3kC0sC9k=";
              }
              {
                name = "cetz";
                version = "0.4.2";
                hash = "sha256-qBIEHqtiMSG/WoXHPC/rQ9VkestSvVNlUwTmAMX1wAs=";
              }
              {
                name = "longops";
                version = "0.2.1";
                hash = "sha256-c11kTQqjcyTcX1EqCxY3IYTKvArbdukBEPeJ4tZXylY=";
              }
              {
                name = "zero";
                version = "0.7.0";
                hash = "sha256-+nvgzG2sV9sgf6z6fJZF/ssg9fceXf/jhEGDtmwpQ1I=";
              }
              {
                name = "mannot";
                version = "0.4.0";
                hash = "sha256-QrYztFl/QMDGkdqfz9jRXUlhHlY8gpgKR5tKWnjlWYY=";
              }
              {
                name = "oxifmt";
                version = "0.2.1";
                hash = "sha256-8PNPa9TGFybMZ1uuJwb5ET0WGIInmIgg8h24BmdfxlU=";
              }
              {
                name = "oxifmt";
                version = "1.0.0";
                hash = "sha256-edTDK5F2xFYWypGpR0dWxwM7IiBd8hKGQ0KArkbpHvI=";
              }
              {
                name = "pinit";
                version = "0.2.2";
                hash = "sha256-D7OwtnkPfyykCBrzpIM5naic13naxDmTxRRMe75su60=";
              }
              {
                name = "tiptoe";
                version = "0.4.0";
                hash = "sha256-awwCPfRXnAaUZ5w3NKt4K22JXzM4QRhTNGoNqrCoB8Q=";
              }
            ];
            fontPaths = [
              "${foundertypeFonts}"
              "${pkgs.newcomputermodern}/share/fonts/opentype/public"
              "${pkgs.cm_unicode}/share/fonts/opentype"
              "${pkgs.nerd-fonts.fira-code}/share/fonts/truetype/NerdFonts/FiraCode"
            ];
          };
          displayLanguage = language;
          participantVisibility = true;
        };
      };
      mkEditorial = language: {
        "editorial.${language}.pdf" = {
          path = hull.document.mkProblemTypstDocument config {
            src = ./document/editorial;
            entry = "${language}.typ";
            fontPaths = [
              "${pkgs.source-han-serif}/share/fonts/opentype/source-han-serif"
              "${pkgs.newcomputermodern}/share/fonts/opentype/public"
            ];
          };
          displayLanguage = language;
        };
      };
      statements = lib.mergeAttrsList (map mkStatement languages);
      editorials = lib.mergeAttrsList (map mkEditorial languages);
    in
    statements // editorials;

  targets = {
    default = hull.problemTarget.common;
    hydro = hull.problemTarget.legacy.hydro.batch {
      statements.zh = "statement.zh.pdf";
      defaultDisplayLanguage = "zh";
      checkerExtName = "cc.cc20o2";
      validatorExtName = "cc.cc20o2";
      testDataExtraFiles."problem.23.hpp" = ./authoring-include/problem.23.hpp;
      judgeExtraFiles = [ "problem.23.hpp" ];
    };
  };
}
