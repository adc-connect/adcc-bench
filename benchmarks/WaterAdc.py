from pyscf import gto, scf


class WaterCcpvdzRhfAdcIteration():
    params = (["adc1", "adc2", "adc2x", "adc3"],
              [2, 4, 7, 10, 15],
              [1e-1, 1e-2, 1e-3, 1e-6])
    param_names = ["method", "n_singlets", "conv_tol"]
    timeout = 120

    def setup(self, *args):
        # Run SCF in pyscf
        mol = gto.M(
            atom='O 0 0 0;'
                 'H 0 0 1.795239827225189;'
                 'H 1.693194615993441 0 -0.599043184453037',
            basis='cc-pvdz',
            unit="Bohr",
            # Disable commandline argument parsing in pyscf
            parse_arg=False,
            dump_input=False,
        )
        scfres = scf.RHF(mol)
        scfres.conv_tol = 1e-13
        scfres.kernel()
        self.scfres = scfres

    def peakmem_iteration(self, method, n_singlets, conv_tol):
        import adcc

        getattr(adcc, method)(self.scfres, n_singlets=n_singlets,
                              conv_tol=conv_tol)

    def time_iteration(self, method, n_singlets, conv_tol):
        import adcc

        getattr(adcc, method)(self.scfres, n_singlets=n_singlets,
                              conv_tol=conv_tol)
