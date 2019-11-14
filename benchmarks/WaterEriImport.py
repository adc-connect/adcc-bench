from pyscf import gto, scf


class WaterEriImport:
    params = (["cc-pvdz", "cc-pvtz"],  # , "cc-pvqz"],
              ["RHF", "UHF"],
              ["o1v1o1v1", "o1o1o1v1", "o1o1v1v1", "o1v1v1v1",
               "o1o1o1o1", "v1v1v1v1"])
    param_names = ["basis", "reference", "block"]

    def setup(self, basis, reference, block):
        import adcc

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
        scfres = getattr(scf, reference)(mol)
        scfres.conv_tol = 1e-8
        scfres.kernel()
        self.scfres = scfres
        self.refstate = adcc.ReferenceState(self.scfres)

    def time_eri_import(self, basis, reference, block):
        self.refstate.cached_eri_blocks = [block]

    def peakmem_eri_import(self, basis, reference, block):
        self.refstate.cached_eri_blocks = [block]
