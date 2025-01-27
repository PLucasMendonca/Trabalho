"use client";

import { useAtomValue } from "jotai";
import { z } from "zod";
import { useForm, Controller, SubmitHandler } from 'react-hook-form';

import { useState, useEffect } from "react";
import {
  Title,
  Text,
  Badge,
  Button,
  Avatar,
  Empty,
  Loader,
  Input,
} from "rizzui";
import cn from "@/utils/class-names";
import {
  dataAtom,
  messageIdAtom,
} from "@/app/shared/support/inbox/message-list";
import { Form } from "@/components/ui/form";
import ActionDropdown from "@/app/shared/support/inbox/action-dropdown";
import MessageBody from "@/app/shared/support/inbox/message-body";
import SimpleBar from "@/components/ui/simplebar";
import { useElementSize } from "@/hooks/use-element-size";
import { useMedia } from "@/hooks/use-media";
import { ChatAPI, ChatProps } from '@/app/lib/chat/fetchChatAPI';
import fetchChatAPI from '@/app/lib/chat/fetchChatAPI';
import { zodResolver } from '@hookform/resolvers/zod';
import { useAppContext } from '@/context';
import fetchEditalUpload, { ChatAPI as IndexAPI } from '@/app/lib/chat/fetchEditalUpload';


type FormValues = {
  message: string;
  edital?: string;
}

interface IndexProps {
  file: File;
}

const schema = z.object({
  message: z.string().min(1, "A mensagem é obrigatória"),
})

export default function MessageDetails({ className }: { className?: string }) {
  const data = useAtomValue(dataAtom);
  const messageId = useAtomValue(messageIdAtom);
  const { importedFile } = useAppContext();
  const [reload, setReload] = useState(false);
  const [loading, setLoading] = useState(false);
  const [disabled, setDisabled] = useState(false);
  const [messages, setMessages] = useState<Array<IndexAPI>>([]);
  const [chat, setChat] = useState<ChatAPI>({ question: '', answer: '' });
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [ref, { width }] = useElementSize();
  const [indexChat, setIndexChat] = useState<string>('');
  const isWide = useMedia("(min-width: 1280px) and (max-width: 1440px)", true);


  function formWidth() {
    if (isWide) return width - 64;
    return width - 44;
  }
  const fetchData = async ({ edital, question }: ChatProps) => {
    try {
      const response = await fetchChatAPI({ edital, question });
      setChat({ answer: response.data[0].answer, question: response.data[0].question });
    } catch (error) {
      setError('Failed to fetch chat');
    }
  };

  const fetchEditalIndexingData = async ({ file }: IndexProps) => {
    setLoading(true);
    setDisabled(true);
    setReload(true);
    try {
      const response = await fetchEditalUpload({ file });
      setMessages(response.data);
      setIndexChat(response.index);
      setLoading(false);
      setDisabled(false)
      setReload(false);
    } catch (error) {
      console.error("Failed to fetch chat", error);
    }
  };


  const message = data.find((m) => m.id === messageId) ?? data[0];
  const initials = `${message?.firstName.charAt(0)}${message?.lastName.charAt(
    0
  )}`;

  // set default selected message when render complete
  useEffect(() => {
    // setFormWidth(width);
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 500); // 500 milliseconds
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (importedFile.length == 0) {
      setDisabled(true);
    }
    if (importedFile.length == 1) {
      fetchEditalIndexingData({ file: importedFile[0].file });
    }

  }, [importedFile]);

  const onSubmit: SubmitHandler<FormValues> = (data) => {
    try {
      setLoading(true);
      setDisabled(true);
      const manageEdital = data.edital ? data.edital : indexChat;
      fetchData({ edital: manageEdital, question: data.message }).then(results => {
        setLoading(false);
        setDisabled(false);
      })
    } catch (error) {
      console.error("Failed to fetch chat", error);
    }
  };


  if (isLoading) {
    return (
      <div
        className={cn(
          "!grid h-full min-h-[128px] flex-grow place-content-center items-center justify-center",
          className
        )}
      >
        <Loader variant="spinner" size="xl" />
      </div>
    );
  }

  if (!message) {
    return (
      <div
        className={cn(
          "!grid h-full min-h-[128px] flex-grow place-content-center items-center justify-center",
          className
        )}
      >
        <Empty
          text="No conversations selected"
          textClassName="mt-4 text-base text-gray-500"
        />
      </div>
    );
  }

  return (
    <div
      className={cn(
        "relative pt-6 lg:rounded-lg lg:border lg:border-muted lg:px-4 lg:py-7 xl:px-5 xl:py-5 2xl:pb-7 2xl:pt-6",
        className
      )}
    >
      <div>
        <header className="flex flex-col justify-between gap-4 border-b border-muted pb-5 3xl:flex-row 3xl:items-center">
          <div className="flex flex-col items-start justify-between gap-3 xs:flex-row xs:items-center xs:gap-6 lg:justify-normal">
            <Title as="h4" className="font-semibold">
              Plataforma inteligente de análise de editais.
            </Title>
          </div>

          <div className="jus flex flex-wrap items-center gap-2.5 sm:justify-end">
            <ActionDropdown className="ml-auto sm:ml-[unset]" />
          </div>
        </header>

        <div className="[&_.simplebar-content]:grid [&_.simplebar-content]:gap-8 [&_.simplebar-content]:py-5">
          <SimpleBar className="@3xl:max-h-[calc(100dvh-34rem)] @4xl:max-h-[calc(100dvh-32rem)] @7xl:max-h-[calc(100dvh-31rem)]">
            <MessageBody messages={messages} question={chat.question} answer={chat.answer} loading={loading} reload={reload} />
          </SimpleBar>
        </div>

        <div
          ref={ref}
          className="grid grid-cols-[32px_1fr] items-start gap-3 rounded-b-lg bg-white @3xl:pt-4 lg:gap-4 lg:pl-0 xl:grid-cols-[48px_1fr] dark:bg-transparent dark:lg:pt-0"
        >
          <figure className="dark:mt-4">
            <Avatar
              name="John Doe"
              initials={initials}
              src="https://isomorphic-furyroad.s3.amazonaws.com/public/avatars-blur/avatar-14.png"
              className="!h-8 !w-8 bg-[#70C5E0] font-medium text-white xl:!h-12 xl:!w-12"
            />
          </figure>
          <div
            className="relative rounded-lg border border-muted bg-gray-50 p-4 2xl:p-5"
            style={{
              maxWidth: formWidth(),
            }}
          >
            <Form<FormValues>
              onSubmit={onSubmit}
              validationSchema={schema}
              resetValues={{ message: '' }}
            >
              {({ control, watch, reset, formState: { errors } }) => {
                return (
                  <div className="relative mb-2.5 flex items-center gap-3.5">
                    <Input
                      label="Mensagem"
                      placeholder="O que você quer perguntar?"
                      variant="flat"
                      className="w-full"
                      type='text'
                      disabled={disabled}

                      {...control.register('message')}

                    />
                    {errors.message && <span>{errors.message.message}</span>}

                    <Button
                      type="submit"
                      className="dark:bg-gray-200 dark:text-white mt-6"
                      disabled={disabled}
                      isLoading={loading}
                    >
                      Enviar
                    </Button>
                  </div>
                );
              }}
            </Form>
          </div>
        </div>
      </div>
    </div>
  );
}

export function DotSeparator({ ...props }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="4"
      height="4"
      viewBox="0 0 4 4"
      fill="none"
      {...props}
    >
      <circle cx="2" cy="2" r="2" fill="#D9D9D9" />
    </svg>
  );
}

type AvatarOptionTypes = {
  avatar: string;
  label: string;
  [key: string]: any;
};

function renderAvatarOptionDisplayValue(option: AvatarOptionTypes) {
  return (
    <div className="flex items-center gap-2">
      <Avatar
        src={option.avatar}
        name={option.label}
        className="!h-6 !w-6 rounded-full"
      />
      <span className="whitespace-nowrap text-xs sm:text-sm">
        {option.label}
      </span>
    </div>
  );
}

function renderPriorityOptionDisplayValue(value: string) {
  switch (value) {
    case "Medium":
      return (
        <div className="flex items-center">
          <Badge color="warning" renderAsDot />
          <Text className="ms-2 font-medium capitalize text-orange-dark">
            {value}
          </Text>
        </div>
      );
    case "Low":
      return (
        <div className="flex items-center">
          <Badge color="success" renderAsDot />
          <Text className="ms-2 font-medium capitalize text-green-dark">
            {value}
          </Text>
        </div>
      );
    case "High":
      return (
        <div className="flex items-center">
          <Badge color="danger" renderAsDot />
          <Text className="ms-2 font-medium capitalize text-red-dark">
            {value}
          </Text>
        </div>
      );
    default:
      return (
        <div className="flex items-center">
          <Badge renderAsDot className="bg-gray-400" />
          <Text className="ms-2 font-medium capitalize text-gray-600">
            {value}
          </Text>
        </div>
      );
  }
}
