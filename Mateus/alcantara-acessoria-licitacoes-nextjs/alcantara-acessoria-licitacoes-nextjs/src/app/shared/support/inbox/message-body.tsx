"use client";

import Image from "next/image";
import { use, useEffect, useState } from "react";
import isEmpty from "lodash/isEmpty";
import { useAtomValue } from "jotai";
import { FiExternalLink } from "react-icons/fi";
import { HiOutlineClipboardDocument } from "react-icons/hi2";
import { PiEye, PiDownloadSimpleBold, PiCheck } from "react-icons/pi";
import { Avatar, Title, Text, Tooltip, Loader } from "rizzui";
import { getRelativeTime } from "@/utils/get-relative-time";
import { useCopyToClipboard } from "@/hooks/use-copy-to-clipboard";
import { DotSeparator } from "@/app/shared/support/inbox/message-details";
import pdfIcon from "@/../public/pdf-icon.svg";
import {
  dataAtom,
  messageIdAtom,
} from "@/app/shared/support/inbox/message-list";
import { ChatAPI } from '@/app/lib/chat/fetchEditalUpload';

interface MessageBodyProps {
  messages: ChatAPI[];
  question: string;
  answer: string;
  loading?: boolean;
  reload?: boolean;

}


export default function MessageBody({ messages, question, answer, loading, reload }: MessageBodyProps) {
  const data = useAtomValue(dataAtom);

  const [list, setMessages] = useState<Array<ChatAPI>>([]);
  const messageId = useAtomValue(messageIdAtom);
  const [isCopied, setIsCopied] = useState(false);
  const [state, copyToClipboard] = useCopyToClipboard();
  const [isLoading, setLoading] = useState(loading);
  const [isReload, setReload] = useState(reload);

  const initialMessage = data.find((m) => m.id === messageId);
  const initials = `${initialMessage?.firstName.charAt(0)}${initialMessage?.lastName.charAt(
    0
  )}`;

  useEffect(() => {
    if (messages) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { question, answer },
      ]);
    }
  }, [question, answer]);

  useEffect(() => {
    if (!isEmpty(messages)) {
      setMessages(prevMessages => [...prevMessages, ...messages]);
    }
  }, [messages]);

  useEffect(() => {
    setLoading(loading);
  }, [loading, isLoading]);

  useEffect(() => {
    if (reload) {
      setMessages([{ question: '', answer: '' }]);
    }
    setReload(reload);
  }, [reload, isReload]);

  const handleCopyToClipboard = () => {
    copyToClipboard(initialMessage?.id as string);
    if (!state.error && state.value) {
      setIsCopied(() => true);
      setTimeout(() => {
        setIsCopied(false);
      }, 3000);
    }
  };

  return (
    <div>
      <div className="grid grid-cols-[32px_1fr] items-start gap-3 lg:gap-4 xl:grid-cols-[48px_1fr]">
        <Avatar
          name="AlcantaAI"
          src={initialMessage?.avatar}
          initials={`AI`}
          className="!h-8 !w-8 bg-[#70C5E0] font-medium text-white xl:!h-11 xl:!w-11"
        />
        <div className="-mt-1.5 lg:mt-0">
          <div className="flex items-center justify-between">
            <Title as="h3" className="text-sm font-medium">
              AlcantaAI
            </Title>
          </div>
          <div className="mt-1.5 items-center gap-2 text-xs text-gray-500 lg:flex">
            <span className="flex items-center lowercase">
              suporte@alcantaramendes.com.br<FiExternalLink className="ml-1 h-2.5 w-2.5" />
            </span>
            <DotSeparator className="hidden lg:block" />
            <span className="mt-1.5 flex items-center lg:mt-0">
              #{initialMessage?.id}{" "}
              <Tooltip
                size="sm"
                rounded="sm"
                placement="top"
                content={isCopied ? "Copied" : "Click to copy"}
              >
                <button type="button" onClick={handleCopyToClipboard}>
                  {isCopied ? (
                    <PiCheck className="ml-1 h-3 w-3" />
                  ) : (
                    <HiOutlineClipboardDocument className="ml-1 h-3 w-3" />
                  )}
                </button>
              </Tooltip>
            </span>
            <DotSeparator className="hidden lg:block" />
            <span>Open {getRelativeTime(new Date(Date.now()))}</span>
          </div>
        </div>
      </div>
      <div className="ml-10 mt-3 grid gap-2 leading-relaxed xl:ml-16 2xl:mt-4">
        {(list.length === 1) && (
          <Text className="font-semibold mb-2">
            {isLoading && (
              <>Carregando...</>
            )}
            {!isLoading && (
              <>Para iniciar preciso que importe um edital em formato PDF no botão "Importar"</>
            )}
          </Text>
        )}
        {list.map((message, index) => (
          <div key={index}>
            <Text className="font-semibold mb-2">{message.question}</Text>
            <Text>{message.answer}</Text>
          </div>
        ))}
        {isLoading && (
          <Loader variant="spinner" size="xl" />
        )}
      </div>
    </div>
  );
}
