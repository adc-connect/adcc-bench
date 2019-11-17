from pyscf import gto, scf

# TODO This is not too sensible as such
#      ... it should be split up into timing / meming the individual steps


class WaterAdcFullrun():
    params = (["sto-3g", "3-21g", "6-31g", "6-31g*", "cc-pvdz"],
              ["adc1", "adc2", "adc2x", "adc3"],
              [2, 4, 7, 10, 15],
              [1e-1, 1e-2, 1e-3, 1e-6])
    param_names = ["basis", "method", "n_singlets", "conv_tol"]
    timeout = 3600 * 10

    def setup(self, basis, *args):
        xyz = """
            C          8.64800        1.07500       -1.71100
            C          9.48200        0.43000       -0.80800
            C          9.39600        0.75000        0.53800
            C          8.48200        1.71200        0.99500
            C          7.65300        2.34500        0.05500
            C          7.73200        2.03100       -1.29200
            H         10.18300       -0.30900       -1.16400
            H         10.04400        0.25200        1.24700
            H          6.94200        3.08900        0.38900
            H          7.09700        2.51500       -2.01800
            N          8.40100        2.02500        2.32500
            N          8.73400        0.74100       -3.12900
            O          7.98000        1.33100       -3.90100
            O          9.55600       -0.11000       -3.46600
            H          7.74900        2.71100        2.65200
            H          8.99100        1.57500        2.99500
        """

        # Run SCF in pyscf
        mol = gto.M(
            atom=xyz,
            basis=basis,
            # Disable commandline argument parsing in pyscf
            parse_arg=False,
            dump_input=False,
        )
        scfres = scf.RHF(mol)
        scfres.conv_tol = 1e-13
        scfres.kernel()
        self.scfres = scfres

    def peakmem_adc(self, basis, method, n_singlets, conv_tol):
        import adcc

        getattr(adcc, method)(self.scfres, n_singlets=n_singlets,
                              conv_tol=conv_tol)

    def time_adc(self, basis, method, n_singlets, conv_tol):
        import adcc

        getattr(adcc, method)(self.scfres, n_singlets=n_singlets,
                              conv_tol=conv_tol)
