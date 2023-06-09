import warnings
from pathlib import Path


def check_ending(fn: str, ending: str = ".csv") -> str:
    """
    Ensures that the filename `fn` ends with `ending`. If not, appends `ending`.

    Args:
        fn: The filename to check.
        ending: The desired ending to check for. Default is ".csv".

    Returns:
        str: The filename with the correct ending.
    """
    return fn if fn.endswith(ending) else fn + ending


def setup_io(
    fn_in: str,
    fn_out: str,
    fn_metadata: str,
    dir_data: str,
    run_name: str,
    dir_exp: str = "experiments",
) -> tuple[Path, Path, Path, Path]:
    """
    Formats the input and output filenames and directories for an experiment.

    Args:
        fn_in: The input filename.
        fn_out: The output filename.
        fn_metadata: The metadata filename.
        dir_data: The directory containing the data.
        run_name: The name of the experiment run.
        dir_exp: The parent directory for the experiment folders. Default is "experiments".

    Returns:
        tuple[Path, Path, Path, Path, Path]: A tuple containing the formatted input, output, and metadata (in and out) paths as well as the .
    """
    # ensure .csv ending consistency
    fn_in, fn_out, fn_metadata = check_ending(fn_in), check_ending(fn_out), check_ending(fn_metadata, ending=".yaml")

    dir_data = Path(dir_data)

    # check if `fn_out` and `fn_metadata` are given as suffixes (start with an underscore) to append to `fn_in`
    # if not assume it is a name in its own right
    if fn_out[0] == "_":
        fn_out = check_ending(fn_in[:-4] + fn_out)
    if fn_metadata[0] == "_":
        fn_metadata = check_ending(fn_in[:-4] + fn_metadata, ending=".yaml")

    if "/" in fn_in:
        fn_in = Path(fn_in)
        warnings.warn(
            f"Using the path supplied to `--input-file` appended to `--dir`, i.e. attempting to read data from {dir_data / fn_in},\nto avoid this warning, specify the path using `--dir` and only the name using `--input-file`\ne.g. `... --dir {(dir_data / fn_in).parent} --input-file {fn_in.name} ...`"
        )

    # generate timestamped experiment folder
    dir_exp = Path(dir_exp) / run_name

    if "/" in fn_out:
        fn_out = Path(fn_out).name
        warnings.warn(
            f"Paths are not supported via `--output-file`, using the name part instead, i.e. attempting to write data to {dir_exp / fn_out}"
        )

    if "/" in fn_metadata:
        fn_metadata = Path(fn_metadata)
        warnings.warn(
            f"Using the path supplied to `--metadata` appended to `--dir`, i.e. attempting to read data from {dir_data / fn_metadata},\nto avoid this warning, specify the path using `--dir` and only the name using `--metadata`\ne.g. `... --dir {(dir_data / fn_metadata).parent} --metadata {fn_metadata.name} ...`"
        )

    # Make the experiment directory
    dir_exp.mkdir(parents=True, exist_ok=True)

    return dir_data / fn_in, dir_exp / fn_out, dir_data / fn_metadata, dir_exp / fn_metadata
