# toothcomb
Scan logs to report interesting entries.

The tool is motivated by checking Error logs for known and new problems.

Problems can be categorised as follows:
- live with (known, but no attempt to fix)
- monitor (watch out for re-occurence to see if a fix should be given priority)
- new/unexplained

Most logs have events on separate lines.
Some logs such as python_exceptions.log are written in blocks with a separator.

A YAML comb specification provides details of known issues and an optional
blocksplit separator.

## Usage
Example comb specification:
~~~~
livewith:
  - label: snmpd
    regexp:
      - Writing core file to /var/opt/crash/core.snmpd
monitor:
  - label: Issue 5437
    regexp:
      - 'Check failed: ''0'', file code/my/path/here.c, line 123'
~~~~
Example of the default toothcomb report:
~~~~
toothcomb check-comb.yaml checks.txt
livewith
========
snmpd: 1

monitor
=======
Issue 5437: 1

unexplained
===========
host-10-32-56-10 CLI[43532]: Check failed: 'function_name.unexpected_attribute == 0' (0x1 == 0x0), file unexpected/path/to/file.c, line 424
~~~~
Example of an annotated report:
~~~~
toothcomb -a check-comb.yaml checks.txt

  host-10-32-56-10 CLI[43532]: Check failed: 'function_name.unexpected_attribute == 0' (0x1 == 0x0), file unexpected/path/to/file.c, line 424
L MTR-be0v81jw0c ms_dump: Writing core file to /var/opt/crash/core.snmpd.145334763. Maximum size: 2615639 kB
M MTR-856t26hgg5 CLI[24345]: Check failed: '0', file code/my/path/here.c, line 123
~~~~
L indicates livewith and M indicates monitor

# Development
Use poetry to create a virtual environment to develop in:
~~~~
poetry install
~~~~
## Running development versions
Use poetry run to run development versions
~~~~
poetry run toothcomb
~~~~

## Running unit tests
~~~~
poetry run pytest
~~~~

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
