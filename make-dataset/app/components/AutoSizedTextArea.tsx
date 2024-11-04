import { useEffect, useRef } from "react";

const AutoSizedTextarea = ({
  defaultValue,
  onchange,
  placeholder,
  className,
}: {
  defaultValue: string;
  onchange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  className?: string;
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      // Reset height to recalculate based on content
      textarea.style.height = "auto";
      // Set the height to match the scroll height based on the initial content
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  }, [defaultValue]); // Runs only on defaultValue change or first render

  return (
    <textarea
      ref={textareaRef}
      defaultValue={defaultValue} // Set the initial content
      placeholder={placeholder || "Type here..."}
      onChange={onchange}
      className={className || ""}
      style={{
        width: "100%",
        minHeight: "50px",
        resize: "none",
        overflow: "hidden",
      }}
    />
  );
};

export default AutoSizedTextarea;
