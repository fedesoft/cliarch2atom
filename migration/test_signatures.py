import math

def normalize_signature(sig):
    iCarpetaMaxima = 10000
    iIncMin = 0.000001

    box, envelop = str(sig).split(".")

    fenvelop = float(f"0.{envelop}")

    zeros = envelop.count("0")

    if zeros:
        envelop = int(round(fenvelop * iCarpetaMaxima))
    else:
        envelop = None
    
    if envelop is not None and envelop:
        return f"{box}/{envelop}"
    return f"{box}"


def get_signature(ini, fin):
    sig_ini = normalize_signature(ini)
    sig_fin = normalize_signature(fin)

    if sig_ini == sig_fin:
        return sig_ini
    else:
        return f"{sig_ini} - {sig_fin}"
    

if __name__ == '__main__':
    
    t1 = get_signature(6759.0017, 6759.0017)
    print(t1)


    # 88544
    t2 = get_signature(5339.0006, 5339.0006)
    print(t2)
    t3 = get_signature(5388.0001, 5388.0003)
    print(t3)
    t4 = get_signature(5388.0006, 5388.0006)
    print(t4)


    t5 = get_signature(10.0018, 10.0018)
    print(t5)
    t6 = get_signature(30.001, 30.001)
    print(t6)
    t7 = get_signature(30.0001, 30.0001)
    print(t7)