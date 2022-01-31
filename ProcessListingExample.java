import java.util.Scanner;

public class ProcessListingExample {

    public static void main(String[] args) throws Exception {
        Processes.ALL_PROCESSES.listProcesses();
    }

    public static enum Processes implements IProcessListingStrategy {
        ALL_PROCESSES;

        private final IProcessListingStrategy processListing = selectProcessListingStrategy();

        @Override
        public void listProcesses() throws Exception {
            processListing.listProcesses();
        }

        private IProcessListingStrategy selectProcessListingStrategy() {
            String OS = System.getProperty("os.name").toLowerCase();
            if (isWindows(OS))
                return new WinProcessListingStrategy();
            else if (isMac(OS))
                return new MacProcessListingStrategy();
            else
                return new LinuxProcessListingStrategy();
        }

        private static boolean isWindows(String OS) {
            return OS.contains("win");

        }

        private static boolean isMac(String OS) {
            return OS.contains("mac");

        }

        private static boolean isUnix(String OS) {
            return (OS.contains("nix") || OS.contains("nux") || OS.contains("aix"));

        }
    }

    static interface IProcessListingStrategy {
        void listProcesses() throws Exception;
    }

    static abstract class AbstractNativeProcessListingStrategy implements IProcessListingStrategy {
        @Override
        public void listProcesses() throws Exception {
            Process process = makeProcessListingProcessBuilder().start();
            Scanner scanner = new Scanner(process.getInputStream());
            while (scanner.hasNextLine()) {
                System.out.println(scanner.nextLine());
            }
            scanner.close();
            process.waitFor();
        }

        protected abstract ProcessBuilder makeProcessListingProcessBuilder();
    }

    static class WinProcessListingStrategy extends AbstractNativeProcessListingStrategy {
        @Override
        protected ProcessBuilder makeProcessListingProcessBuilder() {
            return new ProcessBuilder("cmd", "/c", "tasklist");
        }
    }

    static class LinuxProcessListingStrategy extends AbstractNativeProcessListingStrategy {
        @Override
        protected ProcessBuilder makeProcessListingProcessBuilder() {
            return new ProcessBuilder("ps", "-e");
        }
    }

    static class MacProcessListingStrategy extends AbstractNativeProcessListingStrategy {
        @Override
        protected ProcessBuilder makeProcessListingProcessBuilder() {
            return new ProcessBuilder("ps", "-e");
        }
    }
}