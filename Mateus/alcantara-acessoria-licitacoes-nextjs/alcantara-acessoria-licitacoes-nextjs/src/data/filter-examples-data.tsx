import { StaticImageData } from "next/image";
import Data from "@/utils/data/biddings-example.json";
import govbr from "../../public/govbr.png";

export type Licitacao = {
  thumbnail: StaticImageData;
  srp?: boolean;
  orgaoEntidade?: {
    cnpj: string;
    razaoSocial: string;
    poderId: string;
    esferaId: string;
  };
  anoCompra?: number;
  sequencialCompra?: number;
  dataInclusao?: string;
  dataPublicacaoPncp?: string;
  dataAtualizacao?: string;
  numeroCompra?: string;
  unidadeOrgao: {
    ufNome: string;
    codigoUnidade: string;
    nomeUnidade: string;
    ufSigla: string;
    municipioNome: string;
    codigoIbge: string;
  };
  amparoLegal?: {
    descricao: string;
    nome: string;
    codigo: number;
  };
  dataAberturaProposta?: string;
  dataEncerramentoProposta?: string;
  informacaoComplementar?: string;
  processo?: string;
  objetoCompra: string;
  linkSistemaOrigem?: string;
  justificativaPresencial?: string;
  unidadeSubRogada?: string;
  orgaoSubRogado?: string;
  valorTotalHomologado?: number;
  numeroControlePNCP?: string;
  modalidadeId?: number;
  modoDisputaId?: number;
  modoDisputaNome?: string;
  usuarioNome?: string;
  valorTotalEstimado: number;
  modalidadeNome?: string;
  situacaoCompraId?: number;
  situacaoCompraNome?: string;
  tipoInstrumentoConvocatorioCodigo?: number;
  tipoInstrumentoConvocatorioNome?: string;
  itens?: [
    {
      numeroItem: number;
      descricao: string;
      materialOuServico: string;
      materialOuServicoNome: string;
      valorUnitarioEstimado: number;
      valorTotal: number;
      quantidade: number;
      unidadeMedida: string;
      orcamentoSigiloso: boolean;
      itemCategoriaId: number;
      itemCategoriaNome: string;
      patrimonio?: string;
      codigoRegistroImobiliario?: string;
      criterioJulgamentoId: number;
      criterioJulgamentoNome: string;
      situacaoCompraItem: number;
      situacaoCompraItemNome: string;
      tipoBeneficio: number;
      tipoBeneficioNome: string;
      incentivoProdutivoBasico: boolean;
      dataInclusao: string;
      dataAtualizacao: string;
      temResultado: boolean;
      imagem: number;
    }
  ];
  CategoriaPrincipal?: string;
  Subcategorias?: string[];
};

function injectThumbnail(dataObj: any[]) {
  dataObj.forEach((item) => (item.thumbnail = govbr));

  return dataObj;
}

const [{ data }] = Data;
const dataWithThumbnail = injectThumbnail(data);

export const filterExamplesData: Licitacao[] = dataWithThumbnail;
