< dependencies > 

def main():
    o = Orchestrator()

    n = Load(
        parameter_1 = "",
        parameter_2 = "",
    )

    s1 = Select(
        parameter_1 = "",
        parameter_2 = "",
        (n , "dataset"),
    )

    s2 = Select(
        parameter_1 = "",
        parameter_2 = "",
        (n , "dataset"),
    )

    spl = Split(
        parameter_1 = "",
        parameter_2 = "",
        (s1 , "dataset"),
        (s2, "dataset"),
    )

    ml = Model(
        parameter_1 = "",
        parameter_2 = "",
        (spl, "features_train"),
        (spl, "truth_train"),
    )

    o.add([n, s1, s2, spl, ml])

    o.run()

if __name__ == '__main__':
    main()