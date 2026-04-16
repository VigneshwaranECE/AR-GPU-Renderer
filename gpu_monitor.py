import subprocess

def get_gpu_temperature():
    try:
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"]
        )
        temp = result.decode("utf-8").strip()
        return int(temp)

    except Exception as e:
        return str(e)