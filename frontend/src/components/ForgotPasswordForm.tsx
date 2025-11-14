import type { ComponentProps } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import {
    Field,
    FieldDescription,
    FieldError,
    FieldGroup,
    FieldLabel,
} from '@/components/ui/field';
import { Input } from '@/components/ui/input';
import { Spinner } from '@/components/ui/spinner';
import { forgotPasswordSchema, type ForgotPasswordValues } from '@/auth/schema/forgot-password-schema.ts';
import { useForgotPassword } from '@/auth/useForgotPassword';

export function ForgotPasswordForm({ className, ...props }: ComponentProps<'div'>) {
    const mutation = useForgotPassword();

    const form = useForm<ForgotPasswordValues>({
        resolver: zodResolver(forgotPasswordSchema),
        defaultValues: { email: '' },
    });

    function onSubmit(values: ForgotPasswordValues) {
        mutation.reset();
        mutation.mutate(values, {
            onSuccess: () => {
                form.reset({ email: values.email });
            },
        });
    }

    const formError = mutation.error instanceof Error ? mutation.error.message : null;
    const successMessage = mutation.data?.message ?? (mutation.isSuccess ? 'Si cet email existe, un lien de réinitialisation a été envoyé.' : null);

    return (
        <div className={cn('flex flex-col gap-6', className)} {...props}>
            <Card>
                <CardHeader>
                    <CardTitle>Mot de passe oublié</CardTitle>
                    <CardDescription>
                        Entrez votre adresse email pour recevoir un lien de réinitialisation.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="space-y-6"
                        noValidate
                    >
                        <FieldGroup>
                            <Controller
                                name="email"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="forgot-email">Adresse email</FieldLabel>
                                        <Input
                                            {...field}
                                            id="forgot-email"
                                            type="email"
                                            placeholder="utilisateur@example.com"
                                            aria-invalid={fieldState.invalid}
                                            disabled={mutation.isPending}
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}
                                    </Field>
                                )}
                            />

                            {formError && (
                                <Field data-invalid>
                                    <FieldError errors={[{ message: formError }]} />
                                </Field>
                            )}

                            {successMessage && (
                                <Field>
                                    <p className="text-sm font-medium text-emerald-700">{successMessage}</p>
                                    {mutation.data?.reset_token && (
                                        <FieldDescription>
                                            Token généré : <code>{mutation.data.reset_token}</code>
                                        </FieldDescription>
                                    )}
                                </Field>
                            )}

                            <Field>
                                <Button type="submit" disabled={mutation.isPending} className="w-full">
                                    {mutation.isPending && <Spinner />}
                                    {mutation.isPending ? 'Envoi...' : 'Envoyer le lien'}
                                </Button>
                            </Field>
                        </FieldGroup>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
