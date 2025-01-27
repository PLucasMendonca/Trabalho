import Link from "next/link";
import Image from "next/image";

import facebook from "../../../public/facebook_icon.png";
import instagram from "../../../public/instagram_icon.png";
import x from "../../../public/x_icon.png";

export default function Footer() {
  return (
    <footer className="flex w-full items-center justify-between pt-12">
      <div>
        <div>
          <ul className="flex flex-row gap-4 text-xs pb-4 font-semibold">
            <li>
              <Link href={"#"}>Ajuda</Link>
            </li>
            <li>
              <Link href={"#"}>Dicas de Segurança</Link>
            </li>
            <li>
              <Link href={"#"}>Termos de Uso</Link>
            </li>
            <li>
              <Link href={"#"}>Política de Privacidade</Link>
            </li>
          </ul>
        </div>
        <div className="text-xs">
          <p>Endereço da empresa - Rua teste, Bairro teste</p>
          <p>00000-000 - Cidade teste, UF teste</p>
        </div>
      </div>
      <div>
        <ul className="flex flex-row gap-6">
          <li>
            <Link href={"https://www.facebook.com/"} target={"_blank"}>
              <Image
                src={facebook}
                alt={"Facebook icon"}
                height={20}
                width={20}
              />
            </Link>
          </li>
          <li>
            <Link href={"https://www.instagram.com/"} target={"_blank"}>
              <Image
                src={instagram}
                alt={"Instagram icon"}
                height={20}
                width={20}
              />
            </Link>
          </li>
          <li>
            <Link href={"https://twitter.com/"} target={"_blank"}>
              <Image src={x} alt={"X icon"} height={20} width={20} />
            </Link>
          </li>
        </ul>
      </div>
    </footer>
  );
}
