public class Avvio {
  public static void main(String[] a) throws Exception {
    org.verapdf.gf.foundry.VeraGreenfieldFoundryProvider.initialise();
    org.verapdf.cli.VeraPdfCli.main(a);
  }
}
