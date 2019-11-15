from pyscf import gto, scf

# TODO This is not too sensible as such
#      ... it should be split up into timing / meming the individual steps


class WaterAdcFullrun():
    params = (["cc-pvdz", "cc-pvtz"],
              ["adc1", "adc2", "adc2x", "adc3"],
              [2, 4, 7, 10, 15],
              [1e-1, 1e-2, 1e-3, 1e-6])
    param_names = ["basis", "method", "n_singlets", "conv_tol"]
    timeout = 120

    def setup(self, basis, *args):
        # Run SCF in pyscf
        mol = gto.M(
            atom='O 0 0 0;'
                 'H 0 0 1.795239827225189;'
                 'H 1.693194615993441 0 -0.599043184453037',
            basis=basis,
            unit="Bohr",
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

        adcc.thread_pool.reinit(4, 4)
        getattr(adcc, method)(self.scfres, n_singlets=n_singlets,
                              conv_tol=conv_tol)

    def time_adc(self, basis, method, n_singlets, conv_tol):
        import adcc

        adcc.thread_pool.reinit(4, 4)
        getattr(adcc, method)(self.scfres, n_singlets=n_singlets,
                              conv_tol=conv_tol)
