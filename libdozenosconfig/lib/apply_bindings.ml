(** Apply the Stubs functor to the generated bindings to link the generated
    code into the library. *)
include Bindings.Stubs(Dozenosconfig_bindings)
