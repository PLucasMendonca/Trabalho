import Image from "next/image";
import amLogo from "../../public/am-logo.png";

interface IconProps extends React.SVGProps<SVGSVGElement> {
  iconOnly?: boolean;
}

export default function Logo({ iconOnly = false, ...props }: IconProps) {
  return <Image src={amLogo} alt="Alcântara Mendes Logo" width={275} />;
}
