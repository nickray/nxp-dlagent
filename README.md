# nxp-dlagent

[NXP][nxp] keeps certain documentation and software behind a login wall.  
This tool allows downloading such material in an automated fashion.

[nxp]: https://www.nxp.com

### How To Use

The URL scheme is: <https://www.nxp.com/webapp/Download?colCode={col_code}&appType=license>, 
where `col_code` can be, e.g., `UM11126`, `blhost_2.6.2` or `elftosb_5.6.19`.

Command: `nxp-dl <col_code>`.

Output: the upstream file, e.g. `UM11126.pdf`, or `blhost_2.6.2.zip`.

The script prompts for username and password of an existing NXP account.  
Alternatively, the environment variables `NXP_USERNAME` and `NXP_PASSWORD` can be set.

### Install / Requirements

`pip install .` should work, if you have the requirements:

- <https://pypi.org/project/selenium/>
- <https://github.com/mozilla/geckodriver/>


#### License

<sup>The NXP material has properietary licensing, please read the actual license prompt!
<br>
`nxp-dlagent` itself is dual-licensed under both [Apache License, Version 2.0](LICENSE-APACHE) and [MIT License](LICENSE-MIT).</sup>
<br>
<sub>Any contribution you submit for inclusion in the work (as defined in the Apache-2.0 license, e.g., as GitHub pull request) shall be dual-licensed as above, without any additional terms or conditions.</sub>
